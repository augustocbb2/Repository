# File: monitor_changes.py
# Author: Augusto Bastos
# Date: 2024-10-05
# Description: This script monitors changes in cryptocurrency prices and volumes by comparing new data with average data. It generates alerts if significant changes are detected and logs them into a file. The script also maintains the average price and volume for each ticker and provides functions to calculate initial averages from the first 5 minutes of data and update the averages over time.
# Additionally, the avg_data calculation is delayed until the 6th iteration if no prior data exists in the database.
# Requirements: json, psycopg2, datetime
# Dependencies: Data fetched from external sources (e.g., API, Kafka)
import time
import json
import psycopg2
from datetime import datetime, timedelta
import psycopg2


# Function to monitor price and volume changes and generate alerts if necessary
def monitor_changes(new_data, avg_data):
    alerts = []
    for ticker, values in new_data.items():
        price = values['price']
        volume = values['volume']
        
        # Initialize avg_data for new tickers
        if ticker not in avg_data:
            avg_data[ticker] = {
                'price_avg': price,
                'volume_avg': volume
            }
            continue  # Skip checking the first time since we don't have previous data
        
        # Get previous price and volume averages
        prev_price = avg_data[ticker]['price_avg']
        prev_volume = avg_data[ticker]['volume_avg']
        
        # Calculate price and volume changes
        price_change = ((price - prev_price) / prev_price) * 100 if prev_price != 0 else 0
        volume_change = ((volume - prev_volume) / prev_volume) * 100 if prev_volume != 0 else 0
        
        # Check for significant changes in price or volume (greater than 2%)
        if abs(price_change) > 2 or abs(volume_change) > 2:
            alert_msg = (
                f"{datetime.now()}: Significant change detected for {ticker}. "
                f"Price change: {price_change:.2f}%, Volume change: {volume_change:.2f}%"
            )
            alerts.append(alert_msg)
            print(alert_msg)  # Print the alert for real-time feedback
        
        # Update averages with new values
        avg_data[ticker]['price_avg'] = price
        avg_data[ticker]['volume_avg'] = volume
    
    return alerts, avg_data

# Function to save alerts to a log file
def log_alerts(alerts):
    if alerts:
        with open("alerts.txt", "a") as alert_file:
            for alert in alerts:
                alert_file.write(alert + "\n")

# Function to calculate initial averages for the first 5 minutes of data
def calculate_initial_avg_data(conn):
    avg_data = {}
    try:
        with conn.cursor() as cur:
            # Query to get data from the first 5 minutes
            time_threshold = datetime.now() - timedelta(minutes=5)
            query = """
            SELECT ticker, AVG(price) as price_avg, AVG(volume) as volume_avg
            FROM tickers_data
            WHERE timestamp >= %s
            GROUP BY ticker;
            """
            cur.execute(query, (time_threshold,))
            results = cur.fetchall()
            
            # Populate the avg_data dictionary with initial averages
            for row in results:
                ticker, price_avg, volume_avg = row
                avg_data[ticker] = {
                    'price_avg': price_avg,
                    'volume_avg': volume_avg
                }
            print("Initial avg_data calculated from the first 5 minutes of data.")
    except Exception as e:
        print(f"Error calculating initial avg_data: {e}")
    
    return avg_data

# Function to update avg_data periodically based on new data
def update_avg_data(avg_data, new_data):
    for ticker, values in new_data.items():
        price = values['price']
        volume = values['volume']
        
        # If ticker is not in avg_data, initialize it
        if ticker not in avg_data:
            avg_data[ticker] = {
                'price_avg': price,
                'volume_avg': volume
            }
        else:
            # Update the average price and volume using a simple moving average
            avg_data[ticker]['price_avg'] = (avg_data[ticker]['price_avg'] + price) / 2
            avg_data[ticker]['volume_avg'] = (avg_data[ticker]['volume_avg'] + volume) / 2
    
    print("avg_data updated with new data.")
    return avg_data

# Main function to manage the iteration and call initial avg_data calculation after 5 iterations
def data_ingestion_loop(conn, new_data):
    avg_data = {}
    iteration_counter = 0  # Initialize iteration counter

    while True:
        # Increment the iteration counter
        iteration_counter += 1

        # After the 5th iteration, calculate the initial avg_data if it hasn't been done yet
        if iteration_counter >= 6:
            avg_data = calculate_initial_avg_data(conn)
            print("Initial avg_data fetched after 5 iterations.")

            # Update avg_data with the new incoming data
            avg_data = update_avg_data(avg_data, new_data)

            # Monitor for significant changes and generate alerts
            alerts, avg_data = monitor_changes(new_data, avg_data)

            # Log any alerts
            log_alerts(alerts)

            # Simulate a delay between iterations (e.g., to fetch new data periodically)
            time.sleep(60)  # Wait for 1 minute before repeating the loop
