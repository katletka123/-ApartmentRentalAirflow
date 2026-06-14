import psycopg2
import requests
from datetime import datetime
from datetime import date
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import re

def price_and_negotiable_generate(raw_price):
    if "do negocjacji" in raw_price.lower():
        negotiable=True
    else:
        negotiable=False

    tmp_price = re.findall(r"\d+", raw_price)
    price=int("".join(tmp_price))

    return price, negotiable

def date_generate(raw_date):
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
    if "dzisiaj" in raw_date.lower():
        publication_date = datetime.today().date()
        return publication_date
    else:
        date_list = re.search(r"(\d{1,2})\s+([a-ząćęłńóśźż]+)\s+(\d{4})", raw_date.lower())
        if date_list:
            day = int(date_list.group(1))
            month = months[date_list.group(2)]
            year = int(date_list.group(3))
            publication_date = datetime(year, month, day).date()
            return publication_date


def raw_transform_to_silver(data):
    silver_id=data[0]

    tmp_district_and_date=data[1].split(' - ')
    tmp_district=tmp_district_and_date[0].split(',')
    if len(tmp_district)>1:
        silver_district=tmp_district[1]
    else:
        silver_district="unknown"

    silver_date=date_generate(tmp_district_and_date[1])

    price, negotiable = price_and_negotiable_generate(data[2])
    area=data[3]

    silver_data_list=[]
    silver_data_dict = {
        'id': silver_id,
        'silver_district': silver_district,
        'silver_date': silver_date,
        'silver_price': price,
        'silver_area': area,
        'ready_to_negotiate': negotiable
    }
    silver_data_list.append(silver_data_dict)
    return silver_data_list

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("DB_PORT")
)


for i in range(1):
    url = f"https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page={i}&search%5Border%5D=created_at%3Adesc"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    print("Код ответа:", response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    raw_data_list=[]
    boxes = soup.find_all(attrs={'data-testid': 'l-card'})

    for box in boxes:
        id_num = box.get('id')

        district_and_date_box=box.find(attrs={'data-testid': 'location-date'}).text

        raw_price=box.find(attrs={'data-testid': 'ad-price'}).text

        raw_area=box.find(attrs={'color': 'text-global-secondary'}).text
        print(district_and_date_box,raw_price,raw_area, sep=" ----")
        # area_tmp=raw_area[0].split(" ")
        # area_tmp_coma=area_tmp[0].replace(',','.')
        # price_tmp=raw_price.split(" ")
        # price_tmp_split=price_tmp[0]+price_tmp[1]
        # price_for_m2=round(int(price_tmp_split)/float(area_tmp_coma),2)
        # price_per_meter=f"{price_for_m2} zł/m2"

        raw_data_dict = {
            'id': id_num,
            'raw_date_and_district': district_and_date_box,
            'raw_price': raw_price,
            'raw_area': raw_area
        }
        raw_data_list.append(raw_data_dict)






    create_raw_table="""
        CREATE TABLE IF NOT EXISTS raw_apartments (
        id INTEGER PRIMARY KEY,
        date_and_district VARCHAR(100),
        price VARCHAR(100),
        area  VARCHAR(100),
        ingesting_date DATE DEFAULT NOW()
    );
    """

    create_silver_table= """
        CREATE TABLE IF NOT EXISTS silver_apartments (
        id INTEGER PRIMARY KEY,
        district VARCHAR(100) NOT NULL,
        date VARCHAR(100),
        price_zl VARCHAR(100),
        area  VARCHAR(100),
        ready_to_negotiate BOOLEAN
    );
    """

    insert_raw_table="""
        INSERT INTO raw_apartments (id, date_and_district, price, area)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO 
        UPDATE SET
            date_and_district=EXCLUDED.date_and_district,
            price=EXCLUDED.price,
            area=EXCLUDED.area;
            """

    insert_silver_table="""
        INSERT INTO silver_apartments (id, district, date, price_zl, area, ready_to_negotiate)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO
        UPDATE SET
            district=EXCLUDED.district,
            date=EXCLUDED.date,
            price_zl=EXCLUDED.price_zl,
            area=EXCLUDED.area,
            ready_to_negotiate=EXCLUDED.ready_to_negotiate;
            """
    cursor = conn.cursor()

    cursor.execute(create_raw_table)
    cursor.execute(create_silver_table)

    conn.commit()

    for data in raw_data_list:
        cursor.execute(
            insert_raw_table,
            (data['id'], data['raw_date_and_district'], data['raw_price'], data['raw_area'])
        )
    today=date.today()

    cursor.execute(
        "SELECT * FROM raw_apartments WHERE ingesting_date=%s",
        (today,)
    )
    data_from_raw = cursor.fetchall()
    for el in data_from_raw:
        silver_data_list=raw_transform_to_silver(el)
        for data in silver_data_list:
            cursor.execute(
                insert_silver_table,
                (data['id'], data['silver_district'], data['silver_date'], data['silver_price'], data['silver_area'],data['ready_to_negotiate'])
            )

    conn.commit()