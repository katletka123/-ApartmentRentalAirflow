INSERT INTO raw_apartments (id, date_and_district, price, area, link)
VALUES (
    %(id)s,
    %(date_and_district)s,
    %(price)s,
    %(area)s,
    %(link)s
)
ON CONFLICT (id) DO
UPDATE SET
    date_and_district=EXCLUDED.date_and_district,
    price=EXCLUDED.price,
    area=EXCLUDED.area,
    link=EXCLUDED.link;