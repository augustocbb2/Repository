import json
import requests
from kafka import KafkaProducer
import time

# Load ticker names from tickers.json
with open('tickers.json') as f:
    tickers_data = json.load(f)
tickers = tickers_data['tickers']



# Function to fetch data from CoinGecko API
def fetch_ticker_data(ticker):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'ids': ticker
    }
    response = requests.get(url, params=params)
    print(f"Response for {ticker}: {response.status_code}")
    if response.status_code == 200:
        return response.json()[0]  # Assuming that the first item in the list is the required data
    else:
        print(f"Failed to retrieve data for {ticker}, status code: {response.status_code}")
        return None

# Function to send data to Kafka
def send_data(producer):
    for ticker in tickers:
        data = fetch_ticker_data(ticker)
        if data:
            print(f"Sending data for {ticker}: {data}")
            producer.send('coin_prices', data)
            time.sleep(1)  # Introduce a small delay to avoid overloading the API or Kafka

# Main logic
def producer():
    # Set up Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=['redpanda:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON and then encode it as bytes
    )
    try:
        while True:
            send_data(producer)  # Continuously fetch and send data to Kafka
            time.sleep(60)  # Wait for 1 minute before the next data fetch cycle
    except KeyboardInterrupt:
        print("Stopping producer.")
    finally:
        producer.close()
