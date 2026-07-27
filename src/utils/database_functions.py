import os
from pathlib import Path

import psycopg2
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


def load_sql(relative_path: str) -> str:
    sql_path = Path(__file__).resolve().parent.parent / "source_queries" / relative_path
    with open(sql_path, "r", encoding="utf-8") as file:
        return file.read()

conn = get_connection()


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


def execute_fetchall(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        data_from_raw = cursor.fetchall()
    return data_from_raw
