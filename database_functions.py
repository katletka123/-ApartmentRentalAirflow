import psycopg2
import os
def get_connection():
    return psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("DB_PORT")
)

def execute_many(conn, query, data_list):
    with conn.cursor() as cursor:
        cursor.executemany(
            query,
            data_list
        )
    conn.commit()

def execute_whis_commit(conn, query):
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()

def execute_and_fethall(conn, query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        data_from_raw = cursor.fetchall()
    return data_from_raw

