from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import os
import random

BASE_PATH = "/opt/airflow/data/outputs"

# 1️⃣ EXTRACT
def extract_carts():
    url = "https://fakestoreapi.com/carts"
    response = requests.get(url)
    response.raise_for_status()

    df = pd.json_normalize(response.json())

    os.makedirs(BASE_PATH, exist_ok=True)
    df.to_csv(f"{BASE_PATH}/carts_raw.csv", index=False)

# 2️⃣ GENERATE SYNTHETIC DATA
def generate_synthetic_carts():
    df = pd.read_csv(f"{BASE_PATH}/carts_raw.csv")
    df["date"] = pd.to_datetime(df["date"])

    synthetic_dfs = []

    for i in range(1, 6):  # genera 5 días adicionales
        temp = df.copy()
        temp["id"] = temp["id"] + (i * 1000)
        temp["date"] = temp["date"] + pd.to_timedelta(i, unit="D")
        synthetic_dfs.append(temp)

    df_extended = pd.concat([df] + synthetic_dfs, ignore_index=True)
    df_extended.to_csv(f"{BASE_PATH}/carts_extended.csv", index=False)

# 3️⃣ TRANSFORM
def transform_carts():
    df = pd.read_csv(f"{BASE_PATH}/carts_extended.csv")

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    df.to_parquet(f"{BASE_PATH}/carts_transformed.parquet", index=False)

# DAG
with DAG(
    dag_id="fake_store_etl_synthetic",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["fake_store", "etl", "synthetic_data"],
) as dag:

    extract = PythonOperator(
        task_id="extract_carts",
        python_callable=extract_carts
    )

    generate = PythonOperator(
        task_id="generate_synthetic_data",
        python_callable=generate_synthetic_carts
    )

    transform = PythonOperator(
        task_id="transform_carts",
        python_callable=transform_carts
    )

    extract >> generate >> transform
