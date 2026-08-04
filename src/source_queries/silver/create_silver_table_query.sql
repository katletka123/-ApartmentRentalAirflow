CREATE TABLE IF NOT EXISTS silver_apartments (
    id INTEGER PRIMARY KEY,
    district VARCHAR(100) NOT NULL,
    date DATE,
    price_zl NUMERIC,
    area_m2 NUMERIC,
    ready_to_negotiate BOOLEAN,
    link TEXT
);
