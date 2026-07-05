import psycopg2
import matplotlib.pyplot as plt
from pydantic import color

from database_functions import get_connection
import numpy as np

select_from_silver="""
    WITH tmp_table AS(
        SELECT district, price_zl/area_m2 AS price_per_m2
        FROM silver_apartments
    )
    SELECT district, AVG(price_per_m2)
    FROM tmp_table
    GROUP BY district
"""
area_and_price_per_m2="""
    SELECT area_m2, price_zl/area_m2 AS price_per_m2
    FROM silver_apartments
    WHERE area_m2 IS NOT NULL
        AND price_zl IS NOT NULL
        AND area_m2>0
"""
negotiation="""
    SELECT ready_to_negotiate, COUNT(*)
    FROM silver_apartments
    GROUP BY ready_to_negotiate
"""
def price_per_m2_and_area(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows=cur.fetchall()
    areas=[]
    prices_per_m2=[]
    for row in rows:
        areas.append(float(row[0]))
        prices_per_m2.append(float(row[1]))
    plt.figure(figsize=(10, 6))
    plt.scatter(
        areas,
        prices_per_m2,
        alpha=1,
        color="#F6D3DB"
    )
    k, b = np.polyfit(areas, prices_per_m2, 1)

    x_reg = np.array([min(areas), max(areas)])
    y_reg = k * x_reg + b

    plt.plot(
        x_reg,
        y_reg,
        color="red",
        linewidth=2,
        label=f"y = {k:.2f}x + {b:.2f}"
    )
    plt.title("Цена за м² в зависимости от площади квартиры")
    plt.xlabel("Площадь квартиры (м²)")
    plt.ylabel("Цена за м² (PLN)")

    plt.grid(True)

    plt.show()

    cur.close()
    conn.close()

def negotiate(query):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute(query)
    rows=cur.fetchall()
    labels = []
    values=[]
    for negotiation, count in rows:
        if negotiation is True:
            labels.append("Yes")
        else:
            labels.append("No")
        values.append(count)
    plt.figure(figsize=(6, 6))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=("#F6D3DB", "#BDB9B5")
    )

    plt.title("Ready to negotiate")
    plt.axis("equal")

    plt.show()

    cur.close()
    conn.close()

def avg_price_per_m2_district(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    districts=[]
    prices=[]
    for row in rows:
        districts.append(row[0])
        prices.append(row[1])
    plt.bar(
        districts,
        prices,
        color="#F6D3DB"
    )
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.title("AVG price per m2 for districts")
    plt.xlabel("district")
    plt.ylabel("price zł")
    plt.show()
    cur.close()
    conn.close()

avg_price_per_m2_district(select_from_silver)
