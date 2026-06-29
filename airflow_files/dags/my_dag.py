from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def hello_world():
    print("Hello from Airflow DAG!")


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="my_dag",
    default_args=default_args,
    description="Simple working DAG",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["example"],
) as dag:

    task_hello = PythonOperator(
        task_id="hello_task",
        python_callable=hello_world,
    )

    task_hello

