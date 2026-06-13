import psycopg2
import requests
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import re



def date_generate(row_date):
    months = {
        "stycznia": 1,
        "lutego": 2,
        "marca": 3,
        "kwietnia": 4,
        "maja": 5,
        "czerwca": 6,
        "lipca": 7,
        "sierpnia": 8,
        "września": 9,
        "październik": 10,
        "listopada": 11,
        "grudnia": 12
    }
    # if "dzisiaj" in date:
    #     date = datetime.today().date()
    #     return date
    # else:
    #     date_list = re.search(r"(\d{1,2})\s+([a-ząćęłńóśźż]+)\s+(\d{4})", row_date.lower())
    #     if date_list:
    #         day = int(date_list.group(1))
    #         month = months[date_list.group(2)]
    #         year = int(date_list.group(3))
    #         date = datetime(year, month, day).date()
    #         return date




load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("DB_PORT")
)


for i in range(1,6):
    url = f"https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page={i}&search%5Border%5D=created_at%3Adesc"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    print("Код ответа:", response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    data_lists=[]
    row_data_list=[]
    boxes = soup.find_all(attrs={'data-testid': 'l-card'})

    for box in boxes:
        district_and_date_box=box.find(attrs={'data-testid': 'location-date'}).text.strip().lower().split(" - ")

        # date= date_generate(district_and_date_box[1])

        tmp_district= district_and_date_box[0].split(",")
        if len(tmp_district)==2:
            district=tmp_district[1]
        else:
            district="unknown"

        price=box.find(attrs={'data-testid':'ad-price'}).text.strip()

        area=box.find(attrs={'color':'text-global-secondary'}).text.strip().split(" - ")

        area_tmp=area[0].split(" ")
        area_tmp_coma=area_tmp[0].replace(',','.')
        price_tmp=price.split(" ")
        price_tmp_split=price_tmp[0]+price_tmp[1]
        price_for_m2=round(int(price_tmp_split)/float(area_tmp_coma),2)
        price_per_meter=f"{price_for_m2} zł/m2"

        id_num=box.get('id')

        row_data = {
            'id': id_num,
            'row_district': tmp_district,
            'row_date': district_and_date_box[1],
            'row_price': price,
            'row_area': area[0]
        }
        row_data_list.append(row_data)

        # data_list={
        #     'id': id_num,
        #     'district':district,
        #     'date': date,
        #     'price': price,
        #     'area': area[0],
        #     'price_per_meter': price_per_meter
        # }
        # data_lists.append(data_list)

    create_row_table="""
        CREATE TABLE IF NOT EXISTS row_apartments (
        id INTEGER PRIMARY KEY,
        row_district VARCHAR(100) NOT NULL,
        row_date VARCHAR(100),
        row_price VARCHAR(100),
        row_area  VARCHAR(100)
    );
    """

    # create_silver_table= """
    #     CREATE TABLE IF NOT EXISTS apart (
    #     id INTEGER PRIMARY KEY,
    #     district VARCHAR(100) NOT NULL,
    #     date VARCHAR(100),
    #     price VARCHAR(100),
    #     area  VARCHAR(100),
    #     price_per_meter VARCHAR(100)
    # );
    # """

    insert_row_table="""
        INSERT INTO row_apartments (id, row_district, row_date, row_price, row_area)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO 
        UPDATE SET
            row_district=EXCLUDED.row_district,
            row_date=EXCLUDED.row_date,
            row_price=EXCLUDED.row_price,
            row_area=EXCLUDED.row_area;
            """

    # insert_silver_table="""
    #     INSERT INTO apart (id, district, date, price, area, price_per_meter)
    #     VALUES (%s, %s, %s, %s, %s, %s)
    #     ON CONFLICT (id) DO
    #     UPDATE SET
    #         district=EXCLUDED.district,
    #         date=EXCLUDED.date,
    #         price=EXCLUDED.price,
    #         area=EXCLUDED.area,
    #         price_per_metr=EXCLUDED.price_per_meter;
    #         """
    cursor = conn.cursor()

    cursor.execute(create_row_table)
    # cursor.execute(create_silver_table)

    conn.commit()

    for data in row_data_list:
        cursor.execute(
            insert_row_table,
            (data['id'], data['row_district'], data['row_date'], data['row_price'], data['row_area'])
        )


    conn.commit()