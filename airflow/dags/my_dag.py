from airflow.decorators import dag, task
import pendulum

local_tz = pendulum.timezone("Europe/Warsaw")


@dag(
    schedule="10 0 * * *",
    start_date=pendulum.datetime(2026, 1, 1, tz=local_tz),
    catchup=False,
    tags=["example"],
)
def my_first_dag():
    @task
    def extract():
        return {"data": 42}

    @task
    def transform(data: dict):
        return data["data"] * 2

    @task
    def load(value):
        print(f"Loaded value: {value}")

    load(transform(extract()))


my_first_dag()
