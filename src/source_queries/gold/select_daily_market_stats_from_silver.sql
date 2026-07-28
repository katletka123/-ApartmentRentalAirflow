SELECT  date,
        ROUND(AVG(price_zl),2) as avg_price,
        ROUND(AVG(area_m2),2) as avg_area,
        ROUND(AVG(price_zl/area_m2),2) as avg_price_per_m2,
        COUNT(*) as new_apartments_count
FROM silver_apartments
GROUP BY date
ORDER BY date DESC;