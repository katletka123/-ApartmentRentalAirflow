CREATE TABLE IF NOT EXISTS gold_daily_market_stats (
    date DATE PRIMARY KEY,
    avg_price NUMERIC,
    avg_area NUMERIC,
    avg_price_per_m2 NUMERIC,
    new_apartments_count NUMERIC
);
