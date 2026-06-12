import psycopg2
import requests
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import re



def date_generate(row_date):
    mounths = {
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
    if "dzisiaj" in row_date:
        date = datetime.today().date()
        return date
    else:
        date_list = re.search(r"(\d{1,2})\s+([a-ząćęłńóśźż]+)\s+(\d{4})", row_date.lower())
        if date_list:
            day = int(date_list.group(1))
            mounth = mounths[date_list.group(2)]
            year = int(date_list.group(3))
            date = datetime(year, mounth, day).date()
            return date




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
    boxes = soup.find_all(attrs={'data-testid': 'l-card'})

    for box in boxes:
        district_and_date_box=box.find(attrs={'data-testid': 'location-date'}).text.strip().lower().split(" - ")

        date= date_generate(district_and_date_box[1])

        tmp_district= district_and_date_box[0].split(",")
        district=tmp_district[1]

        price=box.find(attrs={'data-testid':'ad-price'}).text.strip()

        area=box.find(attrs={'color':'text-global-secondary'}).text.strip().split(" - ")

        area_tmp=area[0].split(" ")
        area_tmp_coma=area_tmp[0].replace(',','.')
        price_tmp=price.split(" ")
        price_tmp_split=price_tmp[0]+price_tmp[1]
        price_for_m2=round(int(price_tmp_split)/float(area_tmp_coma),2)
        price_per_metr=f"{price_for_m2} zł/m2"

        id_num=box.get('id')

        data_list={
            'id': id_num,
            'district':district,
            'date': date,
            'price': price,
            'area': area[0],
            'price_per_metr': price_per_metr
        }
        data_lists.append(data_list)



    create_table="""
        CREATE TABLE IF NOT EXISTS apart (
        id INTEGER PRIMARY KEY,
        district VARCHAR(100) NOT NULL,
        date VARCHAR(100),
        price VARCHAR(100),
        area  VARCHAR(100),
        price_per_metr VARCHAR(100)
    );
    """

    insert_table="""
        INSERT INTO apart (id, district, date, price, area, price_per_metr)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO 
        UPDATE SET
            district=EXCLUDED.district,
            date=EXCLUDED.date,
            price=EXCLUDED.price,
            area=EXCLUDED.area,
            price_per_metr=EXCLUDED.price_per_metr;
    """

    cursor = conn.cursor()

    cursor.execute(create_table)

    conn.commit()

    for data in data_lists:
        cursor.execute(
            insert_table,
            (data['id'], data['district'], data['date'], data['price'], data['area'], data['price_per_metr'])
        )


    conn.commit()