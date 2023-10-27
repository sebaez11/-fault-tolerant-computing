FROM apache/airflow:2.3.3


ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/"
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
