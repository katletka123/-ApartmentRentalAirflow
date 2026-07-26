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