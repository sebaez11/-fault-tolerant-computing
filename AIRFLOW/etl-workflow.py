from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import ccxt
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

# Define el DAG (Directed Acyclic Graph)
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 13),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'bitcoin_info',
    default_args=default_args,
    schedule_interval=timedelta(minutes=1),
)

# Tarea para obtener el precio de Bitcoin
def get_bitcoin_price():
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']
    return price

get_price_task = PythonOperator(
    task_id='get_bitcoin_price',
    python_callable=get_bitcoin_price,
    dag=dag,
)

# Tarea para almacenar el precio de Bitcoin en SQLite
def store_bitcoin_price():
    price = get_bitcoin_price()
    conn = sqlite3.connect("bitcoin_prices.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO prices (price, timestamp) VALUES (?, ?)", (price, timestamp))
    conn.commit()
    conn.close()

store_price_task = PythonOperator(
    task_id='store_bitcoin_price',
    python_callable=store_bitcoin_price,
    dag=dag,
)

# Tarea para generar y mostrar el gráfico
def plot_bitcoin_prices():
    conn = sqlite3.connect("bitcoin_prices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, price FROM prices ORDER BY timestamp")
    data = cursor.fetchall()
    conn.close()
    timestamps, prices_text = zip(*data)
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]
    prices = [float(price) for price in prices_text]
    sorted_data = sorted(zip(timestamps, prices), key=lambda x: x[0])
    timestamps, prices = zip(*sorted_data)
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, prices, marker='o')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio del Bitcoin (USDT)')
    plt.title('Histórico de Precios del Bitcoin')
    plt.grid()
    plt.savefig(Path("bitcoin_prices.png"))
    plt.close()

plot_price_task = PythonOperator(
    task_id='plot_bitcoin_prices',
    python_callable=plot_bitcoin_prices,
    dag=dag,
)

# Define el orden de ejecución de las tareas
get_price_task >> store_price_task >> plot_price_task

if __name__ == "__main__":
    dag.cli()
