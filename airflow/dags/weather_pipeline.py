from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "nassim",
    "start_date": datetime(2026, 5, 1),
}

with DAG(
    dag_id="weather_pipeline",
    default_args=default_args,
    schedule="0 6 * * *",
    catchup=False,
) as dag:

    ingestion = BashOperator(
        task_id="ingestion",
        bash_command="python /opt/airflow/project/ingest.py"
    )

    silver = BashOperator(
        task_id="silver_transform",
        bash_command="python /opt/airflow/project/silver_transform.py"
    )

    gold = BashOperator(
        task_id="gold_transform",
        bash_command="python /opt/airflow/project/gold_transform.py"
    )

    quality = BashOperator(
        task_id="quality_checks",
        bash_command="python /opt/airflow/project/quality_checks.py"
    )

    ingestion >> silver >> gold >> quality