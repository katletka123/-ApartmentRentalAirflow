INSERT INTO raw_apartments (id, district_and_date, price, area, link)
VALUES (
    %(id)s,
    %(district_and_date)s,
    %(price)s,
    %(area)s,
    %(link)s
)
ON CONFLICT (id) DO
UPDATE SET
    district_and_date=EXCLUDED.district_and_date,
    price=EXCLUDED.price,
    area=EXCLUDED.area,
    link=EXCLUDED.link;