CREATE MATERIALIZED VIEW IF NOT EXISTS area_and_price_per_m2_mv AS
SELECT
    area_m2,
    price_zl / area_m2 AS price_per_m2
FROM silver_apartments
WHERE
    area_m2 IS NOT NULL
    AND price_zl IS NOT NULL
    AND area_m2 > 0;
