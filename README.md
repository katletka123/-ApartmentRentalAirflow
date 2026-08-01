<!-- ========================= -->
<!--           BADGES          -->
<!-- ========================= -->

<h1 align="center">
Apartment Rental ETL Pipeline
</h1>

<p align="center">
ETL pipeline for collecting, processing and analyzing apartment rental listings from OLX
</p>


---

# Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Database Layers](#database-layers)
- [Installing](#installing)
- [Running the Project](#running-the-project)
- [Future Improvements](#future-improvements)

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

| Category | Technologies               |
|------------|----------------------------|
| Language | Python                     |
| Database | PostgreSQL                 |
| Orchestration | Apache Airflow             |
| Containers | Docker                     |
| Scraping | BeautifulSoup and Requests |
| Visualization | Matplotlib                 |
| Version Control | Git & GitHub               |

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
AirFlow DAG
    │
    ▼
Extract task
    │
    ▼
Transform task
    │
    ▼
Load task
    │
    ▼
Analytics task

```

---

# Project Structure

```text
│
├── airflow/
│   ├── config/
│   ├── dags/
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
├── main.py
├── requirements.txt
└── README.md
```

---

# Database Layers

## Raw

Table: `raw_apartments`

Stores original scraped OLX data before transformation

| Column            | Description                                            |
|-------------------|--------------------------------------------------------|
| id                | Unique identifier of the apartment listing                          |
| district_and_date | Raw location and publication date field                |
| price             | Raw apartment price                                    |
| area              | Raw apartment area                                     |
| ingestion_date    | Date and time when data was ingested into the pipeline |
| link              | URL of the original apartment listing                  |
---

## Silver

Table: `silver_apartments`

Contains cleaned and standardized apartment information

| Column              | Description                  |
|---------------------|------------------------------|
| id                  | Unique identifier of the apartment listing
| district            | Apartment district           |
| date                | Publication date             |
| price_zl            | Apartment rental price in PLN                |
| area_m2             | Area in square meters        |
| ready_to_negotiate  | Boolean flag                 |
| link                | URL of the original apartment listing    |

---

## Gold
Tables:

- `gold_district_statistics`
- `gold_daily_market_statistics`

Contains business metrics used for analysis.

Business-ready aggregated statistics.

Examples:

- Average apartment price
- Average price per m²
- Number of listings
- Daily market statistics

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

3.Create `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=my_db
DB_USER=postgres
DB_PASSWORD=password
```



4.Run Docker

```bash
docker compose up -d --build
```

---

# Running the Project

Run ETL

```bash
python main.py
```

---

# Example Output

The pipeline generates:

- Average apartment price by district
- Average price per square meter
- Apartment publication trends
- Market statistics

---

# Future Improvements

- CI/CD using GitHub Actions
- Unit tests
- Cloud deployment
- Interactive dashboard
- Data quality monitoring

---

# Author

**Anastasiya Kazlova**
