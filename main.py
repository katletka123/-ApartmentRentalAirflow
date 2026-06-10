import psycopg2
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os

load_dotenv()

conn = psycopg2.connect(
    db_host=os.getenv("host"),
    database=os.getenv("database"),
    db_user=os.getenv("user"),
    db_password=os.getenv("password")
)

for i in range(1,4):
    url = f"https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page={i}&search%5Border%5D=created_at%3Adesc"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    print("Код ответа:", response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    data_lists=[]
    boxes = soup.find_all(attrs={'data-testid': 'l-card'})

    for box in boxes:
        dist_and_date=box.find(attrs={'data-testid': 'location-date'}).text.strip().split(" - ")
        date=dist_and_date[1]
        tmp_district=dist_and_date[0].split(",")
        district=tmp_district[1]

        price=box.find(attrs={'data-testid':'ad-price'}).text.strip()

        area=box.find(attrs={'color':'text-global-secondary'}).text.strip().split(" - ")

        id_num=box.get('id')

        data_list={
            'id': id_num,
            'district':district,
            'date': date,
            'price': price,
            'area': area[0]
        }
        data_lists.append(data_list)

    for data in data_lists:
        print(data)

    create_table="""
        CREATE TABLE IF NOT EXISTS apart (
        id INTEGER PRIMARY KEY,
        district VARCHAR(100) NOT NULL,
        date VARCHAR(100),
        price VARCHAR(100),
        area  VARCHAR(100)
    );
    """

    insert_table="""
        INSERT INTO apart (id, district, date, price, area)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO 
        UPDATE SET
            district=EXCLUDED.district,
            date=EXCLUDED.date,
            price=EXCLUDED.price,
            area=EXCLUDED.area;
    """

    cursor = conn.cursor()

    cursor.execute(create_table)

    conn.commit()

    for data in data_lists:
        cursor.execute(
            insert_table,
            (data['id'], data['district'], data['date'], data['price'], data['area'])
        )


    conn.commit()