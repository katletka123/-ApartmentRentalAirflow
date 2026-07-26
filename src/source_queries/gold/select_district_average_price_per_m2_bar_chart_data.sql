WITH tmp_table AS(
    SELECT district, price_zl/area_m2 AS price_per_m2
    FROM silver_apartments
)
SELECT district, AVG(price_per_m2) as avg_price_per_m2
FROM tmp_table
GROUP BY district
ORDER BY avg_price_per_m2 DESC;