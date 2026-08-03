CREATE MATERIALIZED VIEW IF NOT EXISTS daily_market_stats_mv AS
SELECT
    date,
    ROUND(AVG(price_zl), 2) AS avg_price,
    COUNT(*) AS new_apartments_count
FROM silver_apartments
GROUP BY date
ORDER BY date DESC;
