# Usa a imagem do Apache Airflow como base
FROM apache/airflow:2.8.1

# Instala o provedor do Apache Spark para o Apache Airflow
RUN pip install apache-airflow-providers-apache-spark

USER airflow

# Define o ponto de entrada para inicializar o banco de dados do Airflow e iniciar o servidor web e o agendador
ENTRYPOINT [ "bash", "-c", "/entrypoint airflow db init && (/entrypoint airflow webserver & /entrypoint airflow scheduler)" ]

# Define um comando vazio para ser substituído em tempo de execução, se necessário
CMD []
