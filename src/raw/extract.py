import time
import random

from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from src.utils.parsing_utils import date_generate


YESTERDAY = datetime.today().date() - timedelta(days=1)
PAGE_COUNT = 3


def date_separate(date_and_district):
    district_date_parts = date_and_district.split(" - ")
    date = date_generate(district_date_parts[1])
    return date


def is_new_box(box):
    district_and_date_box = box.find(attrs={"data-testid": "location-date"}).text
    result = date_separate(district_and_date_box)
    if result is None:
        return False
    else:
        box_date = result

    if box_date == YESTERDAY:
        return True
    else:
        return False


def get_new_boxes():
    new_boxes = []
    for page in range(1, PAGE_COUNT):
        url = f"https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page={page}&search%5Border%5D=created_at%3Adesc"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        boxes = soup.find_all(attrs={"data-testid": "l-card"})
        for box in boxes:
            if is_new_box(box):
                new_boxes.append(box)
        time.sleep(random.randint(1, 10))
        print("hello cat")
    return new_boxes


def raw_list_generate(boxes):
    raw_data_list = []
    for box in boxes:
        id = box.get("id")
        district_and_date_box = box.find(attrs={"data-testid": "location-date"}).text
        price = box.find(attrs={"data-testid": "ad-price"}).text
        area = box.find(attrs={"color": "text-global-secondary"}).text
        link = box.find("a")["href"]
        raw_data_dict = {
            "id": id,
            "district_and_date": district_and_date_box,
            "price": price,
            "area": area,
            "link": link,
        }
        raw_data_list.append(raw_data_dict)
    return raw_data_list
