<h1 align="center">
Apartment Rental ETL Pipeline
</h1>

<p align="center">
ETL pipeline for collecting, processing and analyzing apartment rental listings from OLX
</p>


---

# Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Database Layers](#database-layers)
- [Installing](#installing)
- [Running the Project](#running-the-project)
- [Example Output](#example-output)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

# Overview

This project implements an end-to-end ETL pipeline for collecting and analyzing apartment rental listings from OLX.

The pipeline automatically extracts raw listing data using Requests and BeautifulSoup, processes and cleans the data, stores it in a layered PostgreSQL data warehouse, and creates analytical tables for market analysis.

The workflow is orchestrated using Apache Airflow DAGs, providing automated and scheduled execution of the ETL process.

The project demonstrates practical Data Engineering skills, including:

- Web Scraping
- ETL Pipeline Development
- Data Cleaning and Transformation
- SQL and PostgreSQL
- Data Warehouse Architecture (Raw / Silver / Gold layers)
- Workflow Orchestration with Apache Airflow
- Containerization with Docker
- Data Visualization

---

# Tech Stack

| Category        | Technologies                             |
|-----------------|------------------------------------------|
| Language        | Python                                   |
| Database        | PostgreSQL                               |
| Orchestration   | Apache Airflow                           |
| Containers      | Docker                                   |
| Scraping        | BeautifulSoup and Requests               |
| Visualization   | Matplotlib                               |
| Version Control | Git & GitHub                             |
| CI/CD           | GitHub Actions (pre-commit checks on pr) |
---


#  Architecture

```text
    OLX
     │
     ▼
Requests + BeautifulSoup
     │
     ▼
PostgreSQL raw layer
     │
     ▼
Python Transformation
     │
     ▼
PostgreSQL silver layer
     │
     ▼
SQL Aggregation
     │
     ▼
PostgreSQL gold layer
     │
     ▼
Matplotlib Analytics
```

---

#  Workflow

```text
DAG: olx_apartments_etl (daily, 00:10 UTC)

1. create_tables            — ensure raw & silver tables exist

2. load_raw_data             — scrape OLX, insert into raw layer

3. transform_raw_to_silver   — clean & normalize raw → silver

4. refresh_gold_daily_market_stats — aggregate silver → gold

5. build_gold_plots  — generate analytics charts
     │
     ├─ price_per_m2_and_area_plot
     ├─ negotiate_pie_chart
     ├─ avg_price_per_m2_district_bar_chart
     ├─ district_price_heatmap
     └─ daily_average_price_chart
```

---

# Project Structure

```text
│
├── .github/
│    └── workflows/
│        └── check-pre-commit-hooks.yml
│
├── airflow/
│   ├── config/
│   ├── dags/
│   │   └── olx_apartment_pipeline.py
│   │
│   ├── logs/
│   ├── plugins/
│   └── docker-compose.yaml
│
├── src/
│   ├── raw/
│   │   └── extract.py
│   │
│   ├── silver/
│   │   └── transform.py
│   │
│   ├── gold/
│   │   └── plots.py
│   │
│   ├── source_queries/
│   │   ├── raw/
│   │   ├── silver/
│   │   └── gold/
│   │
│   └── utils/
│       ├── database_functions.py
│       └── parsing_utils.py
│
├── requirements.txt
└── README.md
```

---

# Database Layers

## Raw

Table: `raw_apartments`

Stores original scraped OLX data before transformation

| Column            | Data Types            | Description                                            |
|-------------------|-----------------------|--------------------------------------------------------|
| id                | `INTEGER PRIMARY KEY` | Unique identifier of the apartment listing             |
| district_and_date | `VARCHAR`             | Raw location and publication date field                |
| price             | `VARCHAR`             | Raw apartment price                                    |
| area              | `VARCHAR`             | Raw apartment area                                     |
| ingestion_date    | `DATE`                | Date and time when data was ingested into the pipeline |
| link              | `TEXT`                | URL of the original apartment listing                  |
---

## Silver

Table: `silver_apartments`

Contains cleaned and standardized apartment information

| Column              | Data Types             | Description                                |
|---------------------|------------------------|--------------------------------------------|
| id                  | `INTEGER PRIMARY KEY`  | Unique identifier of the apartment listing |
| district            | `VARCHAR`              | Apartment district                         |
| date                | `VARCHAR`              | Publication date                           |
| price_zl            | `NUMERIC`              | Apartment rental price in PLN              |
| area_m2             | `NUMERIC `             | Area in square meters                      |
| ready_to_negotiate  | `BOOLEAN`              | Boolean flag                               |
| link                | `TEXT`                 | URL of the original apartment listing      |

---

## Gold
Materialized views:

`negotiation_mv`

Materialized view containing the number of apartment listings grouped by negotiation availability.

| Column               | Data Type   | Description                                                                     |
|----------------------|-------------|---------------------------------------------------------------------------------|
| ready_to_negotiate   | `BOOLEAN`   | Indicates whether the listing is open to price negotiation (`TRUE` or `FALSE`). |
| count                | `NUMERIC`   | Number of listings with the corresponding negotiation status.                   |


`district_price_mv`


Materialized view containing the number of apartment listings grouped by district and price range (1,000 PLN buckets).

| Column         | Data Types   | Description                                                                 |
|----------------|--------------|-----------------------------------------------------------------------------|
| price_bucket   | `NUMERIC`    | Price range bucket in increments of 1,000 PLN                               |
| district       | `VARCHAR`    | Apartment district                                                          |
| count          | `NUMERIC`    | Number of apartment listings in the corresponding price bucket and district |


`district_average_price_per_m2_mv`


Materialized view containing the average apartment price per square meter for each district.

| Column             | Data Types   | Description                                        |
|--------------------|--------------|----------------------------------------------------|
| district           | `VARCHAR`    | Apartment district                                 |
| avg_price_per_m2   | `NUMERIC`    | Average apartment price per square meter (PLN/m²) |


`daily_market_stats_mv`

Materialized view containing daily apartment market statistics, including average price, and the number of new listings

| Column                 | Data Types   | Description                                          |
|------------------------|--------------|------------------------------------------------------|
| date                   | `DATE`       | Publication date                                     |
| avg_price              | `NUMERIC`    | Average apartment rental price (PLN)                 |
| new_apartments_count   | `NUMERIC`    | Number of new apartment listings published that day  |


`area_and_price_per_m2_mv`

Materialized view containing apartment area and the corresponding price per square meter

| Column        | Data Types   | Description                                   |
|---------------|--------------|-----------------------------------------------|
| area_m2       | `NUMERIC`    | Apartment area in square meters (m²)          |
| price_per_m2  | `NUMERIC`    | Apartment price per square meter (PLN/m²)     |

*Source table:* `silver_apartments`

---

# Installing

1. Clone repository

```bash
git clone https://github.com/katletka123/-ApartmentRentalAirflow
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env`

Example .env values:
```env

APP_DB_USER=app_user
APP_DB_PASSWORD=change_me
APP_DB_NAME=my_db
APP_DB_HOST=postgres-app
APP_DB_PORT=5432
APP_DB_INTERNAL_PORT=5433

POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

FERNET_KEY=
AIRFLOW_UID=

COMPOSE_PROJECT_NAME=airflow

```
FERENT_KEY:
```bash
docker run --rm python:3.11-slim bash -c "pip install cryptography -q && python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
```
AIRFLOW_UID:
```bash
echo $(id -u)
```


# Running the Project

Run ETL

1. Start all services (Airflow, PostgreSQL)
```bash
docker compose up -d --build
```
2. Log in (default credentials: airflow / airflow, unless changed in docker-compose.yaml)
3. Enable and trigger the olx_apartments_etl DAG

The DAG will run automatically on schedule (daily at 00:10), or you can trigger it manually from the UI for an immediate run

---

# Example Output

The pipeline generates the following analytics charts:

### Average Price per m² by District
![Price per m² by district](images/avg_price_per_m2_district_bar_chart.png)

### Negotiable vs Fixed Price Listings
![Negotiation pie chart](images/negotiate_pie_chart.png)

### District Price Heatmap
![District price heatmap](images/district_price_heatmap.png)

### Daily Average Price Trend
![Daily average price](images/daily_average_price_chart.png)

### Average Price Trend
![Daily average price](images/price_per_m2_and_area.png)
---

# Future Improvements

1. Unit tests for extraction, transformation, and loading logic
2. Cloud deployment (e.g. AWS/GCP-hosted Airflow and PostgreSQL)
3. Interactive dashboard (e.g. Streamlit or Grafana)
4. Data quality monitoring and alerting

---

# Author

**Anastasiya Kazlova**
