import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from src.utils.database_functions import execute_fetchall


STEP = 1000
REPORTS_BASE_DIR = "/opt/airflow/reports"


def _get_reports_dir():
    date_str = datetime.now().strftime("%Y-%m-%d")
    reports_dir = os.path.join(REPORTS_BASE_DIR, date_str)
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


def build_price_per_m2_and_area_plot(query, conn):
    rows = execute_fetchall(query, conn)
    areas = []
    prices_per_m2 = []
    for row in rows:
        areas.append(float(row[0]))
        prices_per_m2.append(float(row[1]))
    plt.figure(figsize=(10, 6))
    plt.scatter(areas, prices_per_m2, alpha=1, color="#F6D3DB")
    k, b = np.polyfit(areas, prices_per_m2, 1)

    x_reg = np.array([min(areas), max(areas)])
    y_reg = k * x_reg + b

    plt.plot(x_reg, y_reg, color="red", linewidth=2, label=f"y = {k:.2f}x + {b:.2f}")
    plt.title("Цена за м² в зависимости от площади квартиры")
    plt.xlabel("Площадь квартиры (м²)")
    plt.ylabel("Цена за м² (PLN)")

    plt.grid(True)

    filepath = os.path.join(_get_reports_dir(), "price_per_m2_and_area.png")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()


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
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=("#F6D3DB", "#BDB9B5"),
    )

    plt.title("Ready to negotiate")
    plt.axis("equal")

    filepath = os.path.join(_get_reports_dir(), "negotiate_pie_chart.png")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()


def build_avg_price_per_m2_district_bar_chart(query, conn):
    rows = execute_fetchall(query, conn)

    districts = []
    prices = []
    for row in rows:
        districts.append(row[0])
        prices.append(row[1])
    plt.bar(districts, prices, color="#F6D3DB")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.title("AVG price per m2 for districts")
    plt.xlabel("district")
    plt.ylabel("price zł")

    filepath = os.path.join(
        _get_reports_dir(), "avg_price_per_m2_district_bar_chart.png"
    )
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()


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

    fig, ax = plt.subplots(
        figsize=(1.2 * len(districts) + 3, 0.5 * len(price_buckets) + 3)
    )

    custom_cmap = LinearSegmentedColormap.from_list(
        "pusheen_colour", ["#fff0f5", "#ff69b4", "#c2185b"]
    )
    im = ax.imshow(matrix, cmap=custom_cmap, aspect="auto")

    ax.set_xticks(range(len(districts)))
    ax.set_xticklabels(districts, rotation=45, ha="right")
    ax.set_yticks(range(len(price_buckets)))
    ax.set_yticklabels(labels)

    ax.set_xlabel("District")
    ax.set_ylabel("Price range")
    ax.set_title("Distribution of rental listings: price x district")

    max_val = max(max(row) for row in matrix) if matrix else 0
    for i in range(len(price_buckets)):
        for j in range(len(districts)):
            value = matrix[i][j]
            if value > 0:
                ax.text(
                    j,
                    i,
                    value,
                    ha="center",
                    va="center",
                    color="black" if value < max_val * 0.6 else "white",
                    fontsize=9,
                )

    fig.colorbar(im, ax=ax, label="Количество объявлений")
    plt.tight_layout()

    filepath = os.path.join(_get_reports_dir(), "district_price_heatmap.png")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)


def build_daily_average_price_chart(query, conn):
    rows = execute_fetchall(query, conn)
    dates = []
    prices = []
    counts = []

    for row in rows:
        dates.append(row[0])
        prices.append(float(row[1]))
        counts.append(float(row[2]))

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(
        dates,
        prices,
        marker="o",
        linestyle="-",
        alpha=1,
        color="#F6D3DB",
        label="Average price",
    )
    ax1.set_xlabel("Publication date")
    ax1.set_ylabel("Apartment price")
    ax1.tick_params(axis="y")

    ax2 = ax1.twinx()
    ax2.bar(dates, counts, alpha=0.3, color="#BDB9B5", label="New apartments count")
    ax2.set_ylabel("New apartments count")
    ax2.tick_params(axis="y")

    plt.title("Average apartment price and new listings by publication date")
    fig.autofmt_xdate(rotation=45)
    ax1.grid(True, alpha=0.3)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    fig.tight_layout()

    filepath = os.path.join(_get_reports_dir(), "daily_average_price_chart.png")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
