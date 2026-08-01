INSERT INTO gold_daily_market_stats (
    date,
    avg_price,
    avg_area,
    avg_price_per_m2,
    new_apartments_count
)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (date)
DO UPDATE SET
    avg_price = EXCLUDED.avg_price,
    avg_area = EXCLUDED.avg_area,
    avg_price_per_m2 = EXCLUDED.avg_price_per_m2,
    new_apartments_count = EXCLUDED.new_apartments_count;
