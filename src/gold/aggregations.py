
from src.utils.database_functions import get_connection, execute_commit, execute_fetchall, execute_many
from plots import build_daily_average_price_chart

create_gold_district_stats = """
        CREATE TABLE IF NOT EXISTS gold_district_stats (
        district VARCHAR(100) PRIMARY KEY,
        avg_price VARCHAR(100),
        avg_area  VARCHAR(100),
        avg_price_per_m2 VARCHAR(100),
        apartments_count VARCHAR(100)
    );
    """

create_gold_daily_market_stats = """
        CREATE TABLE IF NOT EXISTS gold_daily_market_stats(
        date DATE PRIMARY KEY,
        avg_price VARCHAR(100),
        avg_area  VARCHAR(100),
        avg_price_per_m2 VARCHAR(100),
        new_apartments_count VARCHAR(100)
    );
    """

select_from_silver_1 = """

        SELECT district, ROUND(AVG(price_zl),2) as avg_price,
               ROUND(AVG(area_m2),2) as avg_area,
               ROUND(AVG(price_zl/area_m2),2) as avg_price_per_m2,
               COUNT(*) as apartments_count
        FROM silver_apartments
        GROUP BY district
        ORDER BY avg_price_per_m2;
"""
insert_gold_table_1 = """
        INSERT INTO gold_district_stats (
            district,
            avg_price,
            avg_area,
            avg_price_per_m2,
            apartments_count
        )
        VALUES (%s, %s, %s, %s, %s)
            """

select_from_silver_2 = """
    SELECT  date,
            ROUND(AVG(price_zl),2) as avg_price,
            ROUND(AVG(area_m2),2) as avg_area,
            ROUND(AVG(price_zl/area_m2),2) as avg_price_per_m2,
            COUNT(*) as new_apartments_count
    FROM silver_apartments
    GROUP BY date
    ORDER BY date DESC;
"""
insert_gold_table_2 = """
        INSERT INTO gold_daily_market_stats (
            date,
            avg_price,
            avg_area,
            avg_price_per_m2,
            new_apartments_count
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (date)
        DO UPDATE SET
            avg_price = EXCLUDED.avg_price,
            avg_area = EXCLUDED.avg_area,
            avg_price_per_m2 = EXCLUDED.avg_price_per_m2,
            new_apartments_count = EXCLUDED.new_apartments_count;
            """

select_daily_average_price = """
SELECT date, avg_price
FROM gold_daily_market_stats
"""
if __name__=="__main__":

    # execute_commit(create_gold_district_stats)
    # execute_commit(create_gold_daily_market_stats)
    #
    # data_from_silver_1=execute_fethall(select_from_silver_1)
    # execute_many(insert_gold_table_1, data_from_silver_1)
    #
    data_from_silver_2=execute_fetchall(select_from_silver_2)
    execute_many(insert_gold_table_2, data_from_silver_2)
    build_daily_average_price_chart(select_daily_average_price)