CREATE TABLE IF NOT EXISTS raw_apartments (
    id INTEGER PRIMARY KEY,
    district_and_date VARCHAR(100),
    price VARCHAR(100),
    area VARCHAR(100),
    link TEXT,
    ingestion_date DATE DEFAULT CURRENT_DATE
);
