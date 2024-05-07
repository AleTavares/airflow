from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import json
import requests
import pandas as pd
from airflow.operators.dummy import DummyOperator

def get_dados_api(**kwargs):
    response = requests.get(kwargs['api'])
    if response.status_code == 200:
        with open('/home/data/dados_api.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        return response.json()  
    else:
        raise Exception(f"Erro ao obter os dados de {kwargs['api']}")

def read_json(**kwargs):
    f = open(kwargs['arquivo'])
    teste= json.load(f)
    df = pd.DataFrame(teste['data'])
    df.to_csv('/home/data/dados_api.csv', sep=';', encoding='utf-8')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=0),
}

with DAG(
    dag_id = 'dadosAPI',
    default_args = default_args,
    description = 'DAG para executar job Spark via Operador Spark',
    catchup = False,
    schedule_interval = '@daily',
    tags = ["spark-submit", "spark-connection"]
) as dag:
    start_task = DummyOperator(task_id='start_task')

    coletaDados = PythonOperator(
            task_id='ingestao',
            python_callable=get_dados_api,
            op_kwargs={
                'api': 'https://api.mfapi.in/mf/118550'
            },
        )

    transforma = PythonOperator(
            task_id='transforma',
            python_callable=read_json,
            op_kwargs={
                'arquivo': '/home/data/dados_api.json'
            },
        )
    end_task = DummyOperator(task_id='end_task')

start_task >> coletaDados >> transforma >> end_task

