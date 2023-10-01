import matplotlib
matplotlib.use('TkAgg')

import ccxt
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from prefect import task, flow


@task
def get_bitcoin_price():
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']
    return price


@task
def store_bitcoin_price(price):
    conn = sqlite3.connect("bitcoin_prices.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO prices (price, timestamp) VALUES (?, ?)", (price, timestamp))
    
    conn.commit()
    conn.close()

@task
def plot_bitcoin_prices():

    conn = sqlite3.connect("bitcoin_prices.db")
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, price FROM prices ORDER BY timestamp")
    data = cursor.fetchall()
    conn.close()

    timestamps, prices_text = zip(*data)

    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    # Convierte los valores de texto en números
    prices = [float(price) for price in prices_text]

    # Ordena los valores en función de la fecha
    sorted_data = sorted(zip(timestamps, prices), key=lambda x: x[0])
    timestamps, prices = zip(*sorted_data)


    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, prices, marker='o')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio del Bitcoin (USDT)')
    plt.title('Histórico de Precios del Bitcoin')
    plt.grid()
    plt.show()


@flow
def bitcoin_info():
    plt.close()
    price = get_bitcoin_price()
    store_bitcoin_price(price)
    plot_bitcoin_prices()

if __name__ == "__main__":

    bitcoin_info.serve(name="bitcoin", cron="* * * * *")