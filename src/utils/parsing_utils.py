import re
from datetime import datetime


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
        "grudnia": 12,
    }
    if "dzisiaj" in raw_date.lower():
        publication_date = datetime.today().date()
        return publication_date
    else:
        date_list = re.search(
            r"(\d{1,2})\s+([a-ząćęłńóśźż]+)\s+(\d{4})", raw_date.lower()
        )
        if date_list:
            day = int(date_list.group(1))
            month = months[date_list.group(2)]
            year = int(date_list.group(3))
            publication_date = datetime(year, month, day).date()
            return publication_date
