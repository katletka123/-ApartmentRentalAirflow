from dotenv import load_dotenv
import silver_function
import raw_function
import database_functions

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


load_dotenv()

conn = database_functions.get_connection()
cursor = conn.cursor()

database_functions.execute_whis_commit(conn, create_raw_table)
database_functions.execute_whis_commit(conn, create_silver_table)

boxes= raw_function.get_new_boxes()

raw_data_list= raw_function.raw_list_generate(boxes)

database_functions.execute_many(conn, raw_function.insert_raw_table,raw_data_list)

data_from_raw = database_functions.execute_and_fethall(conn, silver_function.select_from_raw)

silver_data_list= silver_function.raw_transform_to_silver(data_from_raw)

database_functions.execute_many(conn, silver_function.insert_silver_table, silver_data_list)



#аирфлоу>>забрать с сайта>>роу таблица>>cильвер таблица