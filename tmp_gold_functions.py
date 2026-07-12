import psycopg2
from database_functions import execute_commit,execute_many,execute_fethall

create_gold_table_1="""
        CREATE TABLE IF NOT EXISTS gold_district_stats (
        district VARCHAR(100) PRIMARY KEY,
        avg_price VARCHAR(100),
        avg_area  VARCHAR(100),
        avg_price_per_m2 VARCHAR(100),
        apartments_count VARCHAR(100)
    );
    """

create_gold_table_2="""
        CREATE TABLE IF NOT EXISTS gold_daily_market_stats(
        date VARCHAR(100),
        avg_price VARCHAR(100),
        avg_area  VARCHAR(100),
        avg_price_per_m2 VARCHAR(100),
        new_apartments_count VARCHAR(100)
    );
    """

select_from_silver_1="""

        SELECT district, AVG(price_zl) as avg_price, AVG(area_m2) as avg_area, AVG(price_zl/area_m2) as avg_price_per_m2, COUNT(*) as apartments_count
        FROM silver_apartments
        GROUP BY district
        ORDER BY avg_price_per_m2;
"""
insert_gold_table_1="""
        INSERT INTO gold_district_stats (
            district,
            avg_price,
            avg_area,
            avg_price_per_m2,
            apartments_count
        )
        VALUES (%s, %s, %s, %s, %s)
            """

execute_commit(create_gold_table_1)
execute_commit(create_gold_table_2)
data_from_silver=execute_fethall(select_from_silver_1)
execute_many(insert_gold_table_1, data_from_silver)