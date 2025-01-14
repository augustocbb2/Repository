# File: db_setup.py
# Author: Augusto Bastos
# Date: 2024-10-05
# Description: This script is responsible for setting up the database schema, including creating the 'tickers_data' table and 'ohlcv_daily' materialized view. It also includes functions to refresh the materialized view. The database credentials are read from a JSON file.
# Requirements: psycopg2, json
# Dependencies: PostgreSQL database

import psycopg2
import json

# Function to connect to the PostgreSQL database
def get_db_connection():
    with open('db_credentials.json', 'r') as file:
        db_credentials = json.load(file)

    conn = psycopg2.connect(
        dbname=db_credentials["dbname"],
        user=db_credentials["user"],
        password=db_credentials["password"],
        host=db_credentials["host"],
        port=db_credentials["port"]
    )
    return conn

# Function to create the 'tickers_data' table
def create_tickers_table(conn):
    with conn.cursor() as cur:
        create_table_query = """
        DROP MATERIALIZED VIEW IF EXISTS ohlcv_daily;
        DROP TABLE IF EXISTS tickers_data;
        CREATE TABLE IF NOT EXISTS tickers_data (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(50) NOT NULL,
            price NUMERIC NOT NULL,
            volume NUMERIC NOT NULL,
            timestamp TIMESTAMP NOT NULL
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        # Check if the database connection is active
        cur.execute("SELECT 1;")
        cur.fetchone()
        print("Database connection verified.")
        print("Table 'tickers_data' created or already exists.")

# Function to create the 'ohlcv_daily' materialized view
def create_materialized_view(conn):
    with conn.cursor() as cur:
        create_mv_query = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS ohlcv_daily AS
        WITH first_price AS (
            SELECT
                ticker,
                date_trunc('day', timestamp) AS day,
                price AS open
            FROM
                tickers_data
            WHERE (ticker, timestamp) IN (
                SELECT
                    ticker,
                    MIN(timestamp)
                FROM
                    tickers_data
                GROUP BY ticker, date_trunc('day', timestamp)
            )
        ),
        last_price AS (
            SELECT
                ticker,
                date_trunc('day', timestamp) AS day,
                price AS close
            FROM
                tickers_data
            WHERE (ticker, timestamp) IN (
                SELECT
                    ticker,
                    MAX(timestamp)
                FROM
                    tickers_data
                GROUP BY ticker, date_trunc('day', timestamp)
            )
        )
        SELECT
            td.ticker,
            date_trunc('day', td.timestamp) AS day,
            fp.open,
            MAX(td.price) AS high,
            MIN(td.price) AS low,
            lp.close,
            SUM(td.volume) AS volume
        FROM
            tickers_data td
        LEFT JOIN first_price fp ON td.ticker = fp.ticker AND date_trunc('day', td.timestamp) = fp.day
        LEFT JOIN last_price lp ON td.ticker = lp.ticker AND date_trunc('day', td.timestamp) = lp.day
        GROUP BY
            td.ticker, date_trunc('day', td.timestamp), fp.open, lp.close;
        """
        cur.execute(create_mv_query)
        conn.commit()
        print("Materialized View 'ohlcv_daily' created or already exists.")

# Function to refresh the materialized view
def refresh_materialized_view(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("REFRESH MATERIALIZED VIEW ohlcv_daily;")
            conn.commit()
            print("Materialized view 'ohlcv_daily' refreshed.")
    except Exception as e:
        print(f"Error refreshing the materialized view: {e}")
