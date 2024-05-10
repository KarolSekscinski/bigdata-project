from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'seksc',
    'start_date': datetime(2024, 4, 15),
    'catchup': False
}

dag = DAG(
    'hello_world',
    default_args=default_args,
    schedule=timedelta(days=1)
)

t1 = BashOperator(
    task_id='hello_there',
    bash_command='echo "Hello There"',
    dag=dag
)

t2 = BashOperator(
    task_id='hello_general',
    bash_command='echo "General Kenobi"',
    dag=dag
)

t1 >> t2