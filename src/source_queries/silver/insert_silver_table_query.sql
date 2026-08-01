INSERT INTO silver_apartments (id, district, date, price_zl, area_m2, ready_to_negotiate, link)
VALUES (
    %(id)s,
    %(district)s,
    %(date)s,
    %(price)s,
    %(area)s,
    %(ready_to_negotiate)s,
    %(link)s
)
ON CONFLICT (id) DO
UPDATE SET
    district=EXCLUDED.district,
    date=EXCLUDED.date,
    price_zl=EXCLUDED.price_zl,
    area_m2=EXCLUDED.area_m2,
    ready_to_negotiate=EXCLUDED.ready_to_negotiate,
    link=EXCLUDED.link;
