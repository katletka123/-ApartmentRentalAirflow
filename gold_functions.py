from database_functions import execute_commit,execute_many,execute_fethall
from silver_functions import select_from_raw
import matplotlib.pyplot as plt
from database_functions import get_connection

create_gold_district_stats ="""
        CREATE TABLE IF NOT EXISTS gold_district_stats (
        district VARCHAR(100) PRIMARY KEY,
        avg_price VARCHAR(100),
        avg_area  VARCHAR(100),
        avg_price_per_m2 VARCHAR(100),
        apartments_count VARCHAR(100)
    );
    """

create_gold_daily_market_stats="""
        CREATE TABLE IF NOT EXISTS gold_daily_market_stats(
        date VARCHAR(100),
        avg_price VARCHAR(100),
        avg_area  VARCHAR(100),
        avg_price_per_m2 VARCHAR(100),
        new_apartments_count VARCHAR(100)
    );
    """

select_from_silver_1="""

        SELECT district, ROUND(AVG(price_zl),2) as avg_price,
               ROUND(AVG(area_m2),2) as avg_area,
               ROUND(AVG(price_zl/area_m2),2) as avg_price_per_m2,
               COUNT(*) as apartments_count
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

select_from_silver_2="""
    SELECT  date,
            ROUND(AVG(price_zl),2) as avg_price,
            ROUND(AVG(area_m2),2) as avg_area,
            ROUND(AVG(price_zl/area_m2),2) as avg_price_per_m2,
            COUNT(*) as new_apartments_count
    FROM silver_apartments
    GROUP BY date
    ORDER BY date;
"""
insert_gold_table_2="""
        INSERT INTO gold_daily_market_stats (
            date,
            avg_price,
            avg_area,
            avg_price_per_m2,
            new_apartments_count
        )
        VALUES (%s, %s, %s, %s, %s)
            """
tmp_select_toavg_price_date="""
SELECT date, avg_price
FROM gold_daily_market_stats
"""
# execute_commit(create_gold_district_stats)
# execute_commit(create_gold_daily_market_stats)
#
# data_from_silver_1=execute_fethall(select_from_silver_1)
# execute_many(insert_gold_table_1, data_from_silver_1)
#
# data_from_silver_2=execute_fethall(select_from_silver_2)
# execute_many(insert_gold_table_2, data_from_silver_2)

def avg_price_date(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows=cur.fetchall()
    dates=[]
    prices=[]
    for row in rows:
        dates.append(row[0])
        prices.append(float(row[1]))
    plt.figure(figsize=(10, 6))
    plt.plot(
        dates,
        prices,
        marker='o',
        linestyle='-',
        alpha=1,
        color="#F6D3DB"
    )

    plt.title("Цена за м² в зависимости от площади квартиры")
    plt.xlabel("Площадь квартиры (м²)")
    plt.ylabel("Цена за м² (PLN)")

    plt.grid(True)

    plt.show()

    cur.close()
    conn.close()

avg_price_date(tmp_select_toavg_price_date)