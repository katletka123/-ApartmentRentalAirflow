import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def get_connection():
    return psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("DB_PORT")
)

def load_sql(relative_path: str) -> str:
    sql_path = Path(__file__).resolve().parent.parent / "source_queries" / relative_path
    with open(sql_path, "r", encoding="utf-8") as file:
        return file.read()

create_raw_table = load_sql("raw/create_raw_table_query.sql")

create_silver_table= load_sql("silver/create_silver_table_query.sql")

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


