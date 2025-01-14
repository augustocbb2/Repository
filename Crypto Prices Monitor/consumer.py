# File: consumer.py
# Author: Augusto Bastos
# Date: 2024-10-05
# Description: This script acts as the consumer in a Kafka-Redpanda-based system. It consumes cryptocurrency data from a Kafka topic, processes the data by storing it into a PostgreSQL database, and monitors changes to prices and volumes. 
# The data ingestion is performed via KafkaConsumer, and alerts are logged based on predefined criteria. 
# Requirements: kafka-python, psycopg2, requests, json, monitor_changes module.
# Dependencies: PostgreSQL database and Redpanda for message queueing.

import json
import requests
import psycopg2
from datetime import datetime
from monitor_changes import monitor_changes, log_alerts  # Import the monitoring functions
import time
from kafka import KafkaConsumer

# Function to load database credentials from a JSON file
def load_db_credentials(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to load the tickers to be monitored from a JSON file
def load_tickers(file_path):
    with open(file_path, 'r') as file:
        tickers_data = json.load(file)
        return tickers_data.get("tickers", [])

# Function to insert data into the tickers_data table in PostgreSQL
def insert_data(conn, cur, ticker, price, volume, timestamp):
    insert_query = """
    INSERT INTO tickers_data (ticker, price, volume, timestamp)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(insert_query, (ticker, price, volume, timestamp))
    conn.commit()

# Data ingestion and monitoring function
def data_ingestion(conn, cur, avg_data):
    # Set up the Kafka consumer
    consumer = KafkaConsumer(
        'coin_prices',  # Topic name
        bootstrap_servers=['redpanda:9092'],  # Redpanda address
        auto_offset_reset='earliest',  # Read from the beginning of the log
        enable_auto_commit=True,  # Automatically commit offsets
        group_id='consumer-group',  # Consumer group name
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON messages
    )

    new_data = {}

    # Iterate over messages received from Kafka topic
    for message in consumer:
        data = message.value
        print(f"{datetime.now()} - Data received: {data}")
        if data:
            try:
                # Extract ticker information and relevant fields from the data
                ticker = data['id']
                price = data.get('current_price', 0)
                volume = data.get('total_volume', 0)
                timestamp = datetime.now().isoformat()

                # Insert the data into the PostgreSQL database
                insert_data(conn, cur, ticker, price, volume, timestamp)
                print(f"{timestamp} - Data inserted: {ticker} - Price: {price}, Volume: {volume}")

                # Store new data for change monitoring
                new_data[ticker] = {'price': price, 'volume': volume}

                # Monitor changes and generate alerts
                alerts, avg_data = monitor_changes(new_data, avg_data)
                log_alerts(alerts)  # Log alerts to a file
            except Exception as e:
                print(f"Error processing the data: {e}")
        
    return avg_data

# Main consumer function to handle database connection and ingestion loop
def consumer():
    # Load database connection settings
    db_credentials = load_db_credentials('db_credentials.json')

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=db_credentials["dbname"],
        user=db_credentials["user"],
        password=db_credentials["password"],
        host=db_credentials["host"],
        port=db_credentials["port"]
    )
    cur = conn.cursor()

    # Load the tickers to be monitored
    tickers = load_tickers('tickers.json')

    # Dictionary to store average data for tracking changes
    avg_data = {}

    # Ingestion and monitoring loop
    while True:
        try:
            # Call data ingestion and monitoring function
            avg_data = data_ingestion(conn, cur, avg_data)
            time.sleep(60)  # Wait for 1 minute before repeating
        except KeyboardInterrupt:
            print("Exiting consumer...")
            break

    # Close the database connection
    cur.close()
    conn.close()
