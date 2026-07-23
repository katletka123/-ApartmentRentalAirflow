from datetime import datetime,timedelta
YESTERDAY = datetime.today().date() - timedelta(days=1)
import requests
from bs4 import BeautifulSoup
import re

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

insert_raw_table="""
        INSERT INTO raw_apartments (id, date_and_district, price, area, link)
        VALUES (
                   %(raw_id)s,
                   %(raw_date_and_district)s,
                   %(raw_price)s, 
                   %(raw_area)s,
                   %(raw_link)s
               )
        ON CONFLICT (id) DO 
        UPDATE SET
            date_and_district=EXCLUDED.date_and_district,
            price=EXCLUDED.price,
            area=EXCLUDED.area,
            link=EXCLUDED.link;
            """

def date_separate(date_and_district):
    tmp_district_and_date = date_and_district.split(' - ')
    date = date_generate(tmp_district_and_date[1])
    return date

def is_new_box(box):
    district_and_date_box=box.find(attrs={'data-testid': 'location-date'}).text
    result = date_separate(district_and_date_box)
    if result is None:
        return False
    else:
        box_date=result

    if box_date==YESTERDAY:
        return True
    else:
        return False

def get_new_boxes():
    new_boxes=[]
    for page in range(1,26):
        url = f"https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page={page}&search%5Border%5D=created_at%3Adesc"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        boxes = soup.find_all(attrs={'data-testid': 'l-card'})
        for box in boxes:
            if is_new_box(box):
                new_boxes.append(box)
                page+=1
    return new_boxes

def raw_list_generate(boxes):
    raw_data_list = []
    for box in boxes:
        print("hello")
        id_num = box.get('id')
        raw_district_and_date_box = box.find(attrs={'data-testid': 'location-date'}).text
        raw_price = box.find(attrs={'data-testid': 'ad-price'}).text
        raw_area = box.find(attrs={'color': 'text-global-secondary'}).text
        raw_link=box.find("a")["href"]
        raw_data_dict = {
            'raw_id': id_num,
            'raw_date_and_district': raw_district_and_date_box,
            'raw_price': raw_price,
            'raw_area': raw_area,
            'raw_link': raw_link
        }
        raw_data_list.append(raw_data_dict)
    return raw_data_list

