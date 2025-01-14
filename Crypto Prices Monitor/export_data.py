import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# PostgreSQL database configuration using environment variables
DB_HOST = os.getenv('POSTGRES_HOST')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_PORT = os.getenv('POSTGRES_PORT', 5432)  # Default port is 5432

# Establish connection to PostgreSQL
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
cursor = conn.cursor()
def export_daily_csv_by_ticker():

    # Get the distinct list of tickers
    tickers_query = f"""
    SELECT DISTINCT ticker FROM ohlcv_daily"""
    tickers = pd.read_sql(tickers_query, conn)['ticker'].tolist()

    # Export data for each ticker
    for ticker in tickers:
        query = f"""
        SELECT ticker, day, open, high, low, close
        FROM ohlcv_daily
        WHERE ticker = '{ticker}'
        """
        df = pd.read_sql(query, conn)
        df.to_csv(f'daily_crypto_data_{ticker}.csv', index=False)
        print(f'Daily data exported for {ticker} to daily_crypto_data_{ticker}.csv')

def export_minute_parquet_by_ticker():
    # Get the distinct list of tickers
    tickers_query = "SELECT DISTINCT ticker FROM tickers_data"
    tickers = pd.read_sql(tickers_query, conn)['ticker'].tolist()

    # Export data for each ticker
    for ticker in tickers:
        query = f"""
        SELECT ticker, timestamp, price
        FROM tickers_data
        WHERE ticker = '{ticker}'
        """
        df = pd.read_sql(query, conn)
        df.to_parquet(f'minute_crypto_data_{ticker}.parquet', index=False)
        print(f'Minute data exported for {ticker} to minute_crypto_data_{ticker}.parquet')

if __name__ == '__main__':
    
    export_minute_parquet_by_ticker()
    export_daily_csv_by_ticker()