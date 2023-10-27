import psycopg2

# Establece conexión con la base de datos PostgreSQL
def fetch_prices_from_db():
    # Conexión
    connection = psycopg2.connect(
        host="dpg-cktmh9enfb1c73f728m0-a.oregon-postgres.render.com",
        database="bitcoin_prices_db",
        user="bitcoin_prices_db_user",
        password="cUNfpIY4ggoehwJ2t5gT0Q95Op59MU58"
    )
    
    cursor = connection.cursor()

    # Ejecuta consulta para traer todos los datos de la tabla 'prices'
    cursor.execute("SELECT * FROM prices;")
    
    # Trae todos los registros
    records = cursor.fetchall()

    # Cierra la conexión
    cursor.close()
    connection.close()

    return records

# Ejecuta la función y muestra los datos
if __name__ == "__main__":
    prices_data = fetch_prices_from_db()
    for record in prices_data:
        print(record)

