import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("DB_PORT")
)


create_raw_table="""
        CREATE TABLE IF NOT EXISTS raw_apartments (
        id INTEGER PRIMARY KEY,
        date_and_district VARCHAR(100),
        price VARCHAR(100),
        area  VARCHAR(100),
        ingestion_date DATE DEFAULT CURRENT_DATE
    );
    """

create_silver_table= """
        CREATE TABLE IF NOT EXISTS silver_apartments (
        id INTEGER PRIMARY KEY,
        district VARCHAR(100) NOT NULL,
        date VARCHAR(100),
        price_zl NUMERIC,
        area_m2  NUMERIC,
        ready_to_negotiate BOOLEAN
    );
    """

conn =get_connection()

def execute_many(query, data_list):
    with conn.cursor() as cursor:
        cursor.executemany(
            query,
            data_list
        )
    conn.commit()

def execute_commit(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()

def execute_fethall(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        data_from_raw = cursor.fetchall()
    return data_from_raw

