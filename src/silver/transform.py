import re
import numpy as np
from datetime import datetime


def price_and_negotiable_generate(raw_price):
    if "do negocjacji" in raw_price.lower():
        negotiable = True
    else:
        negotiable = False

    price_matches = re.findall(r"\d[\d\s,.]*", raw_price)
    price=None
    if price_matches:
        price = float(
            price_matches[0]
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
    district_date_parts = date_and_district.split(' - ')
    district_parts = district_date_parts[0].split(',')
    if len(district_parts) > 1:
        silver_district = district_parts[1]
    else:
        return None
    silver_date = date_generate(district_date_parts[1])
    return silver_district, silver_date

def raw_transform_to_silver(raw_data):
    all_transformed_rows = []
    for data in raw_data:
        id = data[0]
        result = date_district_separate(data[1])
        if result is None:
            continue
        district, date = result
        price, negotiable = price_and_negotiable_generate(data[2])
        area_parts = data[3].split(' ')
        area = float(area_parts[0].replace(',', '.'))
        link = data[5]
        silver_data_dict = {
            'id': id,
            'district': district,
            'date': date,
            'price': price,
            'area': area,
            'ready_to_negotiate': negotiable,
            'link': link
        }
        all_transformed_rows.append(silver_data_dict)

    if not all_transformed_rows:
        return []

    prices = [silver_data_dict["price"] for silver_data_dict in all_transformed_rows]
    q_high = np.quantile(prices,0.95)
    q_low = np.quantile(prices,0.05)

    filtered_silver_data_list = [
        silver_data_dict for silver_data_dict in all_transformed_rows
        if q_low <= silver_data_dict["price"] <= q_high
    ]
    return filtered_silver_data_list