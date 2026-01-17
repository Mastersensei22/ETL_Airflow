Este proyecto implementa un pipeline ETL (Extract, Transform, Load) distribuido utilizando Apache Airflow con CeleryExecutor, completamente containerizado mediante Docker Compose. El pipeline consume datos de ventas desde una API externa de e-commerce (Fake Store API), genera datos sintéticos para simular un mayor volumen de información y crecimiento del negocio, aplica transformaciones para análisis y persiste los datos procesados en un formato optimizado csv. 

El objetivo principal del proyecto es demostrar cómo construir un pipeline de datos escalable y cercano a un entorno productivo, utilizando herramientas modernas de ingeniería de datos. 

Para esto use Docker, Airflow, python para los scrips necesarios del ETL.

La idea principal es tomar datos desde cualquier API, extraerlos, trasformarlos y cargarlos para su posterior analisis. 


La arquitectura está completamente containerizada y compuesta por los siguientes componentes:

Apache Airflow Scheduler

Apache Airflow Webserver

Apache Airflow Workers (CeleryExecutor)

Redis como broker de mensajería

PostgreSQL como base de metadatos de Airflow

Volúmenes Docker para almacenamiento persistente de datos

El DAG orquesta las siguientes etapas:

Extracción de datos de ventas desde la Fake Store API

Generación de datos sintéticos para incrementar el volumen

Transformación y enriquecimiento de los datos

Almacenamiento de los datos transformados en formato CSV.

Tecnologías Utilizadas: Python, Apache Airflow, Docker & Docker Compose, CeleryExecutor, Redis, PostgreSQL, Pandas, Fake Store API.

Estructura del proyecto.

fake_store_airflow/
│
├── dags/
│   └── fake_store_etl.py
│
├── data/
│   └── outputs/
│       ├── carts_raw.csv
│       └── carts_transformed.parquet
│
├── docker-compose.yml
├── requirements.txt
└── README.md
