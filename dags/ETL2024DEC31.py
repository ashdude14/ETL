from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator # Airflow has kind of Docker operator? use it after finding in registory.. https://registry.astronomer.io/modules?types=operators
from airflow import Dataset
from pendulum import datetime

@dag(
    dag_id="ETL2024DEC31",
    start_date=datetime(2024, 12, 30), 
    schedule='0 10 * * 1',  # weekly--> cron expression https://crontab.guru/  “At 10:00 on Monday.”
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3}, # Retries can be overridden in the task definition
    tags=["My ETL DAG!"],  # To recognize DAG in more complex project 
)
def ETL2024DEC31():
    start_standalone_server = BashOperator(
        task_id="start_standalone_server",
        bash_command="echo 'Starting standalone server!'",
    )

    perform_web_scraping = BashOperator(
        task_id="perform_web_scraping",
        bash_command="echo 'Performing web scraping!'",
    )

    transformation = BashOperator(
        task_id="transformation",
        bash_command="echo 'Performing data transformation!'",
    )

    loading_to_postgres_server = BashOperator(
        task_id="loading_to_postgres_server",
        bash_command="echo 'Loading to Postgres server!'",
    )

    # Defining task dependencies
    start_standalone_server >> perform_web_scraping >> transformation >> loading_to_postgres_server

# Instantiating the DAG
ETL2024DEC31()
