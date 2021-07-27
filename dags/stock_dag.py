import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
import sys
sys.path.insert(0,"/home/kobe/PycharmProjects/stock_analysis")
from crawl.big5_update import run_crawl
from update.update_predict import  update_model_predict
import pendulum

local_tz = pendulum.timezone("Asia/Taipei")

default_args = {
    'owner': 'Kobe',
    'start_date': datetime(2021, 7, 26, 1, 6 , tzinfo=local_tz),
    'schedule_interval': '@daily',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'tags' : ['stock']
}


with DAG('stock_dag', start_date= datetime(2021, 7, 25 , tzinfo=local_tz), schedule_interval="20 13 * * *", tags=["stock"] ) as dag:
    crawl_web = PythonOperator(
        task_id='crawl_web',
        python_callable=run_crawl,
        provide_context=True
    )

    update_predict = PythonOperator(
        task_id='update_predict',
        python_callable=update_model_predict,
        provide_context=True
    )

    crawl_web >> update_predict