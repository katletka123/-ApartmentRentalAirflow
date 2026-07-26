SELECT (FLOOR(price_zl / %s) * %s)::int AS price_bucket,
        district, COUNT(*) as count
FROM silver_apartments
GROUP BY price_bucket, district
ORDER BY price_bucket, district;