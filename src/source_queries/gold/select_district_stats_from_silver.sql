SELECT district, ROUND(AVG(price_zl),2) as avg_price,
       ROUND(AVG(area_m2),2) as avg_area,
       ROUND(AVG(price_zl/area_m2),2) as avg_price_per_m2,
       COUNT(*) as apartments_count
FROM silver_apartments
GROUP BY district
ORDER BY avg_price_per_m2;