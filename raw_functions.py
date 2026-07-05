from datetime import datetime,timedelta
YESTERDAY = datetime.today().date() - timedelta(days=1)
import requests
from bs4 import BeautifulSoup
from silver_functions import date_district_separate

insert_raw_table="""
        INSERT INTO raw_apartments (id, date_and_district, price, area)
        VALUES (
                   %(raw_id)s,
                   %(raw_date_and_district)s,
                   %(raw_price)s, 
                   %(raw_area)s
               )
        ON CONFLICT (id) DO 
        UPDATE SET
            date_and_district=EXCLUDED.date_and_district,
            price=EXCLUDED.price,
            area=EXCLUDED.area;
            """

def is_new_box(box):
    district_and_date_box=box.find(attrs={'data-testid': 'location-date'}).text
    box_date=date_district_separate(district_and_date_box)[1]
    if box_date==YESTERDAY:
        return True
    else:
        return False

def get_new_boxes():
    new_boxes=[]
    for page in range(1,3):
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

        raw_data_dict = {
            'raw_id': id_num,
            'raw_date_and_district': raw_district_and_date_box,
            'raw_price': raw_price,
            'raw_area': raw_area
        }
        raw_data_list.append(raw_data_dict)
    return raw_data_list

