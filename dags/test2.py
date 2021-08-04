from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator ,PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import pendulum

local_tz = pendulum.timezone("Asia/Taipei")
args = {
    'owner': 'airflow',
    # 'depends_on_past': True,
}
dt = datetime.now()
dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

def should_run(**kwargs):
    print("123")
def two():
    print("56565")


with DAG(
    dag_id='test10',
    schedule_interval='37 17 * * *',
    start_date= dt.astimezone(local_tz) -timedelta(1) ,
    default_args=args,
    tags=['example'],
    concurrency=1000,
    max_active_runs=1000,
) as dag:

    cond = PythonOperator(
        task_id='condition',
        python_callable=should_run,
    )

    cond2 = PythonOperator(
        task_id='condition2',
        python_callable=two,
    )

    cond >> cond2