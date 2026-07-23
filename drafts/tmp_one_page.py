from datetime import datetime,timedelta
YESTERDAY = datetime.today().date() - timedelta(days=1)
import requests
from bs4 import BeautifulSoup
from src.silver.transform import date_district_separate
from urllib.parse import urljoin

def is_new_box(box):
    district_and_date_box=box.find(attrs={'data-testid': 'location-date'}).text
    result = date_district_separate(district_and_date_box)
    if result is None:
        return False
    else:
        box_date=result[1]

    if box_date==YESTERDAY:
        return True
    else:
        return False

def get_new_boxes():
    new_boxes=[]
    for page in range(1, 3):
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

def hohrah(boxes):
    for box in boxes:
        link_part2 = box.find("a")["href"]
        link = urljoin("https://www.olx.pl", link_part2)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        container=soup.find(attrs={'data-testid':'ad-parameters-container'})
        if container is not None:
            params = container.find_all("p")
            for p in params:
                print(p.get_text(strip=True))



boxes=get_new_boxes()
hohrah(boxes)