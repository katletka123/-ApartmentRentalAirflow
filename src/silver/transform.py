from datetime import datetime
import re
import numpy as np

select_from_raw="""
            SELECT * FROM raw_apartments
            WHERE ingestion_date = CURRENT_DATE
"""

insert_silver_table="""
        INSERT INTO silver_apartments (id, district, date, price_zl, area_m2, ready_to_negotiate, link)
        VALUES (
            %(silver_id)s,
            %(silver_district)s, 
            %(silver_date)s, %(silver_price)s, 
            %(silver_area)s, 
            %(ready_to_negotiate)s,
            %(link)s
            )
        ON CONFLICT (id) DO
        UPDATE SET
            district=EXCLUDED.district,
            date=EXCLUDED.date,
            price_zl=EXCLUDED.price_zl,
            area_m2=EXCLUDED.area_m2,
            ready_to_negotiate=EXCLUDED.ready_to_negotiate,
            link=EXCLUDED.link;
            """

def price_and_negotiable_generate(raw_price):
    if "do negocjacji" in raw_price.lower():
        negotiable=True
    else:
        negotiable=False

    tmp_price = re.findall(r"\d[\d\s,.]*", raw_price)

    if tmp_price:
        price = float(
            tmp_price[0]
            .replace(" ", "")
            .replace(",", ".")
        )
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

def date_district_separate(date_and_district):
    tmp_district_and_date = date_and_district.split(' - ')
    tmp_district = tmp_district_and_date[0].split(',')
    if len(tmp_district) > 1:
        silver_district = tmp_district[1]
    else:
        return None
    silver_date = date_generate(tmp_district_and_date[1])
    return silver_district, silver_date

def raw_transform_to_silver(raw_data):
    silver_data_list_tmp = []
    silver_data_list = []
    for data in raw_data:
        silver_id=data[0]
        result = date_district_separate(data[1])
        if result is None:
            continue
        silver_district, silver_date = result
        price, negotiable = price_and_negotiable_generate(data[2])
        tmp_area=data[3].split(' ')
        area=tmp_area[0].replace(',','.')
        link=data[5]
        silver_data_dict = {
            'silver_id': silver_id,
            'silver_district': silver_district,
            'silver_date': silver_date,
            'silver_price': price,
            'silver_area': area,
            'ready_to_negotiate': negotiable,
            'link':link
        }
        silver_data_list_tmp.append(silver_data_dict)
        prices=[silver_data_dict["silver_price"] for silver_data_dict in silver_data_list_tmp]
        q_high=np.quantile(prices,0.95)
        q_low=np.quantile(prices,0.05)
        silver_data_list=[
            silver_data_dict for silver_data_dict in silver_data_list_tmp
            if q_low<=silver_data_dict["silver_price"]<= q_high
        ]
    return silver_data_list