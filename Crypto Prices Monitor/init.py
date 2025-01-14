# File: init.py
# Author: Augusto Bastos
# Date: 2024-10-05
# Description: This script initializes the database setup, starts the producer, consumer, and monitoring services, and runs them in separate threads. It includes the necessary setup to create the tickers_data table, the materialized view, and integrates the functions for calculating and updating the moving average over the last 5 minutes.
# Requirements: threading, producer, consumer, db_setup, psycopg2, monitor_changes
# Dependencies: PostgreSQL database, Kafka/Redpanda services for producer and consumer, monitoring for price and volume changes.

import threading
import producer
import consumer
import db_setup  # The file that contains the database setup functions
import monitor_changes  # The file that contains the monitoring functions
from psycopg2 import OperationalError

# Initialize the database setup
def setup_database():
    try:
        conn = db_setup.get_db_connection()
        db_setup.create_tickers_table(conn)  # Create the tickers_data table
        db_setup.create_materialized_view(conn)  # Create the ohlcv_daily materialized view
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
    finally:
        conn.close()

# Function to start the Producer
def start_producer():
    producer.producer()

# Function to start the Consumer
def start_consumer():
    # Calls the function that handles data ingestion
    consumer.consumer()

# Function to start the monitoring process
def start_monitoring():
    # Database connection is required to monitor data
    conn = db_setup.get_db_connection()

    # This will be the loop to monitor for changes
    new_data = {}  # This would typically be data from your producer or consumer
    try:
        # Initial avg_data calculation could be done here, assuming the first 5 minutes have passed
        avg_data = monitor_changes.calculate_initial_avg_data(conn)

        # Simulating data ingestion loop and monitoring logic
        monitor_changes.data_ingestion_loop(conn, new_data)
    except Exception as e:
        print(f"Error during monitoring: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting database setup, Producer, Consumer, and Monitoring.")

    # Start the database setup
    setup_database()

    # Start the Producer, Consumer, and Monitoring in separate threads
    producer_thread = threading.Thread(target=start_producer)
    consumer_thread = threading.Thread(target=start_consumer)
    monitoring_thread = threading.Thread(target=start_monitoring)

    producer_thread.start()
    consumer_thread.start()
    monitoring_thread.start()

    producer_thread.join()
    consumer_thread.join()
    monitoring_thread.join()
