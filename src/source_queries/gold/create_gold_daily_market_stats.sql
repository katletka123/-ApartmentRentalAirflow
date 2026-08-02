CREATE TABLE IF NOT EXISTS gold_daily_market_stats (
    date DATE PRIMARY KEY,
    avg_price NUMERIC,
    avg_area VARCHAR(100),
    avg_price_per_m2 VARCHAR(100),
    new_apartments_count VARCHAR(100)
);
