import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
import sys
sys.path.insert(0,"/opt/airflow/")
from crawl.big5_update import run_crawl
from update.update_predict import  run_predcit
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

stock_id_list =  ["2330" ,"2603","2609","3481","2303","2409","2317","2002"]


with DAG('stock_dag', start_date= datetime(2021, 7, 29 , tzinfo=local_tz), schedule_interval="00 17 * * *", tags=["stock"] ) as dag:
    crawl_web = PythonOperator(
        task_id='crawl_web',
        python_callable=run_crawl,
        provide_context=True
    )

    update_predict = PythonOperator(
        task_id='update_predict',
        python_callable=run_predcit,
        provide_context=True,
        op_kwargs= {"stock_id_list":stock_id_list}
    )

    crawl_web >> update_predict