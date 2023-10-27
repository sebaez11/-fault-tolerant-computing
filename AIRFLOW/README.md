# Airflow Bitcoin Prices ETL Tutorial

In this tutorial, we'll set up a simple ETL pipeline using Apache Airflow to fetch the current price of Bitcoin from Binance, store it in a PostgreSQL database, and plot the historical prices. 

**1. Create the DAG File**

The `etl-workflow.py` file contains the definition of our Directed Acyclic Graph (DAG) for the ETL process.

- We'll start by importing necessary libraries and setting up the database configurations.
- The `default_args` dictionary contains the default arguments for our DAG, such as the owner and start date.
- The `dag` object represents our workflow. It is scheduled to run every minute.
- We have three main tasks in our DAG:
  1. `get_bitcoin_price`: Fetch the current Bitcoin price from Binance.
  2. `store_bitcoin_price`: Store the fetched price in a PostgreSQL database.
  3. `plot_bitcoin_prices`: Retrieve historical prices from the database and plot them using `matplotlib`.

**2. Docker Configuration**

Our project also uses Docker to containerize the Airflow setup.

- The `Dockerfile` sets up the Airflow environment by starting from the `apache/airflow:2.3.3` base image, setting the Python path, copying the requirements, and installing necessary Python packages.
  
**3. Docker-Compose Configuration**

The `docker-compose-yaml` file defines the services we need to run our Airflow setup.

- We are setting up several services including PostgreSQL, Redis, Airflow Webserver, Scheduler, Worker, Triggerer, and Init.
- Each service has specific configurations like image, environment variables, volumes, etc.
- The Airflow services use the CeleryExecutor, which allows them to distribute task execution across multiple workers.
- Redis acts as the message broker, and PostgreSQL is used as both the metadata and results backend for Airflow.

**To run the project**:

1. Place the `etl-workflow.py` file in the `dags` directory.
2. Build the Docker image:
   ```
   docker-compose build
   ```
3. Start the services:
   ```
   docker-compose up
   ```
4. Access the Airflow web UI by navigating to `http://localhost:8080`.
5. Enable the `bitcoin_info` DAG and monitor its runs.

## Results

![Airflow Dashboard](https://lh3.googleusercontent.com/u/2/drive-viewer/AK7aPaCTTsNTbUlTPsU4B13JNUt6bljOOihRs09qmauU6D2a77Hw7MahIsHgPku5zWiktHXgvYCfAd-hE6Vx3S0Y811XJy6b=w1848-h976)

![Script for visualize db data](https://lh3.googleusercontent.com/u/2/drive-viewer/AK7aPaDOXkrcx-_XKeYukk4b4JV34OLlGjLAWPFNkJURPDexncsjjYn_hJF7Nv9J2j3Ntcz4NKMCNBDciJvEM5jpxvdHOPfsxg=w1848-h976)

**Note**: Make sure to not expose sensitive information like database passwords in your project files. Always use environment variables or secret management tools to handle such information securely.
