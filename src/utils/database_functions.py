import os
from pathlib import Path

import psycopg2
from psycopg2.extensions import connection as PgConnection

from dotenv import load_dotenv


load_dotenv()

def get_connection() -> PgConnection:
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


def execute_many(query, data_list, conn):
    with conn.cursor() as cursor:
        cursor.executemany(
            query,
            data_list
        )


def execute_commit(query, conn):
    with conn.cursor() as cursor:
        cursor.execute(query)


def execute_fetchall(query, conn, params = None):
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        data = cursor.fetchall()
    return data
