import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

def fun1():
    print('hello fun 1')

def fun2():
    print('hello fun 2')


my_dag = DAG(
    dag_id="my_dag_name",
    start_date=datetime.datetime(2021, 1, 1),
    schedule="* * * * *",
)

task1 = PythonOperator(task_id="task1", dag=my_dag, python_callable=fun1)
task2 = PythonOperator(task_id="task2", dag=my_dag, python_callable=fun2)

task1 >> task2