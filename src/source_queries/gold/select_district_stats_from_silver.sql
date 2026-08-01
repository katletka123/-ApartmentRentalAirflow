SELECT
    district,
    ROUND(AVG(price_zl), 2) AS avg_price,
    ROUND(AVG(area_m2), 2) AS avg_area,
    ROUND(AVG(price_zl / area_m2), 2) AS avg_price_per_m2,
    COUNT(*) AS apartments_count
FROM silver_apartments
GROUP BY district
ORDER BY avg_price_per_m2;
