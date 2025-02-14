#!/bin/bash
airflow db upgrade
airflow users create --username "airflow_user" --password "$AIRFLOW_ADMIN_PASSWORD" \
    --role Admin --firstname "Airflow" --lastname "Flowman" --email "airflow@example.com"
