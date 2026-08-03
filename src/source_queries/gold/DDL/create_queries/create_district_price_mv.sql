CREATE MATERIALIZED VIEW IF NOT EXISTS district_price_mv AS
SELECT (FLOOR(price_zl / 1000) * 1000)::int AS price_bucket,
        district, COUNT(*) as count
FROM silver_apartments
GROUP BY price_bucket, district
ORDER BY price_bucket, district;
