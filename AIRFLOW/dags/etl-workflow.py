from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import ccxt
import psycopg2
import matplotlib.pyplot as plt


DATABASE_CONFIG = {
    'dbname': 'bitcoin_prices_db',
    'user': 'bitcoin_prices_db_user',
    'password': 'cUNfpIY4ggoehwJ2t5gT0Q95Op59MU58',
    'host': 'dpg-cktmh9enfb1c73f728m0-a.oregon-postgres.render.com',
    'port': '5432'  # generalmente es 5432 para PostgreSQL
}


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'bitcoin_info',
    default_args=default_args,
    schedule_interval=timedelta(minutes=1),
)

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


def store_bitcoin_price():
    price = get_bitcoin_price()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS prices (price TEXT, timestamp TIMESTAMP);""")
    cursor.execute("INSERT INTO prices (price, timestamp) VALUES (%s, %s)", (price, timestamp))
    conn.commit()
    conn.close()

store_price_task = PythonOperator(
    task_id='store_bitcoin_price',
    python_callable=store_bitcoin_price,
    dag=dag,
)

def plot_bitcoin_prices():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, price FROM prices ORDER BY timestamp")
    data = cursor.fetchall()
    conn.close()
    timestamps, prices_text = zip(*data)
    timestamps = [ts for ts in timestamps]
    prices = [float(price) for price in prices_text]
    sorted_data = sorted(zip(timestamps, prices), key=lambda x: x[0])
    timestamps, prices = zip(*sorted_data)
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, prices, marker='o')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio del Bitcoin (USDT)')
    plt.title('Histórico de Precios del Bitcoin')
    plt.grid()
    #plt.savefig(Path("bitcoin_prices.png"))
    plt.show()

plot_price_task = PythonOperator(
    task_id='plot_bitcoin_prices',
    python_callable=plot_bitcoin_prices,
    dag=dag,
)

get_price_task >> store_price_task >> plot_price_task

if __name__ == "__main__":
    dag.cli()
