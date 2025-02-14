from airflow.decorators import dag, task
from datetime import datetime
# from src.pipelines.mountain_project.clean_and_insert_mp_routes import main

@dag(schedule_interval='@daily', start_date=datetime(2025, 2, 10), tags=["MP"], catchup=False)
def clean_and_insert_mp_routes():
    @task()
    def fetch_mp_routes():
        print("HELLO DAG")