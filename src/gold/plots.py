import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from src.utils.database_functions import execute_fetchall


STEP = 1000

def build_price_per_m2_and_area_plot(query, conn):
    rows = execute_fetchall(query, conn)
    areas = []
    prices_per_m2 = []
    for row in rows:
        areas.append(float(row[0]))
        prices_per_m2.append(float(row[1]))
    plt.figure(figsize=(10, 6))
    plt.scatter(
        areas,
        prices_per_m2,
        alpha = 1,
        color = "#F6D3DB"
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


def build_negotiate_pie_chart(query, conn):
    rows = execute_fetchall(query, conn)
    labels = []
    values = []
    for negotiation, count in rows:
        if negotiation is True:
            labels.append("Yes")
        else:
            labels.append("No")
        values.append(count)
    plt.figure(figsize=(6, 6))

    plt.pie(
        values,
        labels = labels,
        autopct = "%1.1f%%",
        startangle = 90,
        colors = ("#F6D3DB", "#BDB9B5")
    )

    plt.title("Ready to negotiate")
    plt.axis("equal")

    plt.show()


def build_avg_price_per_m2_district_bar_chart(query, conn):
    rows = execute_fetchall(query, conn)

    districts = []
    prices = []
    for row in rows:
        districts.append(row[0])
        prices.append(row[1])
    plt.bar(
        districts,
        prices,
        color = "#F6D3DB"
    )
    plt.xticks(rotation = 45, ha = 'right')
    plt.tight_layout()
    plt.title("AVG price per m2 for districts")
    plt.xlabel("district")
    plt.ylabel("price zł")
    plt.show()


def build_district_price_heatmap(query, conn, params):
    rows = execute_fetchall(query, conn, params)

    price_buckets = sorted({row[0] for row in rows})
    districts = sorted({row[1] for row in rows})

    bucket_idx = {b: i for i, b in enumerate(price_buckets)}
    district_idx = {d: j for j, d in enumerate(districts)}

    matrix = [[0] * len(districts) for _ in price_buckets]
    for price_bucket, district, cnt in rows:
        i = bucket_idx[price_bucket]
        j = district_idx[district]
        matrix[i][j] = cnt
    labels = [f"{b}-{b + STEP}" for b in price_buckets]

    fig, ax = plt.subplots(figsize=(1.2 * len(districts) + 3, 0.5 * len(price_buckets) + 3))

    custom_cmap = LinearSegmentedColormap.from_list(
        "pusheen_colour", ["#fff0f5", "#ff69b4", "#c2185b"]
    )
    im = ax.imshow(matrix, cmap=custom_cmap, aspect="auto")

    ax.set_xticks(range(len(districts)))
    ax.set_xticklabels(districts, rotation=45, ha="right")
    ax.set_yticks(range(len(price_buckets)))
    ax.set_yticklabels(labels)

    ax.set_xlabel("Район")
    ax.set_ylabel("Ценовой диапазон")
    ax.set_title("Распределение объявлений об аренде: цена x район")

    max_val = max(max(row) for row in matrix) if matrix else 0
    for i in range(len(price_buckets)):
        for j in range(len(districts)):
            value = matrix[i][j]
            if value > 0:
                ax.text(j, i, value, ha = "center", va = "center",
                        color = "black" if value < max_val * 0.6 else "white",
                        fontsize = 9)

    fig.colorbar(im, ax = ax, label = "Количество объявлений")
    plt.tight_layout()
    plt.show()


def build_daily_average_price_chart(query, conn):
    rows = execute_fetchall(query, conn)
    dates = []
    prices = []
    for row in rows:
        dates.append(row[0])
        prices.append(float(row[1]))
    plt.figure(figsize = (10, 6))
    plt.plot(
        dates,
        prices,
        marker = 'o',
        linestyle = '-',
        alpha = 1,
        color = "#F6D3DB"
    )

    plt.title("Average apartment price by publication Date")
    plt.xlabel("Publication date")
    plt.ylabel("Apartment price")

    plt.xticks(rotation = 45)
    plt.grid(True)

    plt.show()
