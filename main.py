from contextlib import closing

from src.silver.transform import raw_transform_to_silver
from src.raw.extract import get_new_boxes, raw_list_generate
from src.utils.database_functions import (
    execute_commit,
    execute_many,
    execute_fetchall,
    load_sql,
    get_connection,
)
from src.gold.plots import (
    build_price_per_m2_and_area_plot,
    build_negotiate_pie_chart,
    build_avg_price_per_m2_district_bar_chart,
    build_district_price_heatmap,
    build_daily_average_price_chart,
    STEP,
)


def create_tables():
    create_raw_table = load_sql("raw/create_raw_table_query.sql")
    create_silver_table = load_sql("silver/create_silver_table_query.sql")

    with closing(get_connection()) as conn:
        try:
            execute_commit(create_raw_table, conn)
            execute_commit(create_silver_table, conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def load_raw_data():
    boxes = get_new_boxes()
    raw_data_list = raw_list_generate(boxes)
    insert_raw_table = load_sql("raw/insert_raw_table_query.sql")

    with closing(get_connection()) as conn:
        try:
            execute_many(insert_raw_table, raw_data_list, conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def transform_raw_to_silver():
    select_from_raw = load_sql("silver/select_from_raw_query.sql")
    insert_silver_table = load_sql("silver/insert_silver_table_query.sql")

    with closing(get_connection()) as conn:
        try:
            data_from_raw = execute_fetchall(select_from_raw, conn)
            silver_data_list = raw_transform_to_silver(data_from_raw)
            execute_many(insert_silver_table, silver_data_list, conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def refresh_gold_daily_market_stats():
    create_daily_market_stats = load_sql("gold/create_gold_daily_market_stats.sql")
    select_daily_market_stats = load_sql(
        "gold/select_daily_market_stats_from_silver.sql"
    )
    insert_gold_daily_market_stats = load_sql("gold/insert_gold_daily_market_stats.sql")

    with closing(get_connection()) as conn:
        try:
            execute_commit(create_daily_market_stats, conn)
            daily_market_data = execute_fetchall(select_daily_market_stats, conn)
            execute_many(insert_gold_daily_market_stats, daily_market_data, conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def build_gold_plots():
    select_area_and_price_per_m2_plot_data = load_sql(
        "gold/select_area_and_price_per_m2_plot_data.sql"
    )
    select_negotiation_plot_data = load_sql("gold/select_negotiation_plot_data.sql")
    select_district_average_price_per_m2_bar_chart_data = load_sql(
        "gold/select_district_average_price_per_m2_bar_chart_data.sql"
    )
    select_district_price_heatmap_data = load_sql(
        "gold/select_district_price_heatmap_data.sql"
    )
    select_daily_average_price_data = load_sql("gold/select_daily_average_price.sql")

    with closing(get_connection()) as conn:
        build_price_per_m2_and_area_plot(select_area_and_price_per_m2_plot_data, conn)
        build_negotiate_pie_chart(select_negotiation_plot_data, conn)
        build_avg_price_per_m2_district_bar_chart(
            select_district_average_price_per_m2_bar_chart_data, conn
        )
        build_district_price_heatmap(
            select_district_price_heatmap_data, conn, (STEP, STEP)
        )
        build_daily_average_price_chart(select_daily_average_price_data, conn)


if __name__ == "__main__":
    create_tables()
    load_raw_data()
    transform_raw_to_silver()
    refresh_gold_daily_market_stats()
    build_gold_plots()
