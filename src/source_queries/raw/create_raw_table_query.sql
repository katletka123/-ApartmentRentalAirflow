CREATE TABLE IF NOT EXISTS raw_apartments (
    id INTEGER PRIMARY KEY,
    date_and_district VARCHAR(100),
    price VARCHAR(100),
    area  VARCHAR(100),
    link  TEXT,
    ingestion_date DATE DEFAULT CURRENT_DATE
);
