CREATE MATERIALIZED VIEW IF NOT EXISTS daily_market_stats_mv AS
SELECT
    date,
    ROUND(AVG(price_zl), 2) AS avg_price,
    ROUND(AVG(area_m2), 2) AS avg_area,
    ROUND(AVG(price_zl / area_m2), 2) AS avg_price_per_m2,
    COUNT(*) AS new_apartments_count
FROM silver_apartments
GROUP BY date
ORDER BY date DESC;
