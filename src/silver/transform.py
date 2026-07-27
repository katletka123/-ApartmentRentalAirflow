import re

import numpy as np

from src.utils.parsing_utils import date_generate


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
