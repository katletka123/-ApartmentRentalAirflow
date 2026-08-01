import inspect

from contextlib import closing
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from functools import wraps

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


def handle_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with closing(get_connection()) as conn:
            try:
                result = func(*args, conn=conn, **kwargs)
                conn.commit()
                return result
            except Exception:
                conn.rollback()
                raise

    original_sig = inspect.signature(func)
    visible_params = [
        p for name, p in original_sig.parameters.items() if name != "conn"
    ]
    wrapper.__signature__ = original_sig.replace(parameters=visible_params)
    return wrapper


@handle_connection
def create_tables(conn):
    create_raw_table = load_sql("raw/create_raw_table_query.sql")
    create_silver_table = load_sql("silver/create_silver_table_query.sql")
    execute_commit(create_raw_table, conn)
    execute_commit(create_silver_table, conn)


@handle_connection
def load_raw_data(conn):
    boxes = get_new_boxes()
    raw_data_list = raw_list_generate(boxes)
    insert_raw_table = load_sql("raw/insert_raw_table_query.sql")
    execute_many(insert_raw_table, raw_data_list, conn)


@handle_connection
def transform_raw_to_silver(conn):
    select_from_raw = load_sql("silver/select_from_raw_query.sql")
    insert_silver_table = load_sql("silver/insert_silver_table_query.sql")
    data_from_raw = execute_fetchall(select_from_raw, conn)
    silver_data_list = raw_transform_to_silver(data_from_raw)
    execute_many(insert_silver_table, silver_data_list, conn)


@handle_connection
def refresh_gold_daily_market_stats(conn):
    create_daily_market_stats = load_sql("gold/create_gold_daily_market_stats.sql")
    select_daily_market_stats = load_sql(
        "gold/select_daily_market_stats_from_silver.sql"
    )
    insert_gold_daily_market_stats = load_sql("gold/insert_gold_daily_market_stats.sql")
    execute_commit(create_daily_market_stats, conn)
    daily_market_data = execute_fetchall(select_daily_market_stats, conn)
    execute_many(insert_gold_daily_market_stats, daily_market_data, conn)


@handle_connection
def build_gold_plots(conn):
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
    build_price_per_m2_and_area_plot(select_area_and_price_per_m2_plot_data, conn)
    build_negotiate_pie_chart(select_negotiation_plot_data, conn)
    build_avg_price_per_m2_district_bar_chart(
        select_district_average_price_per_m2_bar_chart_data, conn
    )
    build_district_price_heatmap(select_district_price_heatmap_data, conn, (STEP, STEP))
    build_daily_average_price_chart(select_daily_average_price_data, conn)


def task_failure_alert(context):
    task_id = context["task_instance"].task_id
    print(f"Task {task_id} failed")


default_args = {
    "owner": "katletka",
    "on_failure_callback": task_failure_alert,
}


with DAG(
    dag_id="olx_apartments_etl",
    default_args=default_args,
    description="Пайплайн: OLX -> raw -> transform -> gold",
    start_date=datetime(2024, 1, 1),
    schedule="10 0 * * *",
    catchup=False,
    tags=["olx", "apartments", "etl"],
) as dag:
    create_tables_task = PythonOperator(
        task_id="create_tables",
        python_callable=create_tables,
    )

    load_raw_data_task = PythonOperator(
        task_id="load_raw_data",
        python_callable=load_raw_data,
    )

    transform_raw_to_silver_task = PythonOperator(
        task_id="transform_raw_to_silver",
        python_callable=transform_raw_to_silver,
    )

    refresh_gold_daily_market_stats_task = PythonOperator(
        task_id="refresh_gold_daily_market_stats",
        python_callable=refresh_gold_daily_market_stats,
    )

    build_gold_plots_task = PythonOperator(
        task_id="build_gold_plots",
        python_callable=build_gold_plots,
    )










    (
        create_tables_task
        >> load_raw_data_task
        >> transform_raw_to_silver_task
        >> refresh_gold_daily_market_stats_task
        >> build_gold_plots_task
    )
