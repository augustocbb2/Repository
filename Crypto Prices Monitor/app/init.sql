-- init.sql

-- Criação da tabela 'tickers_data'
CREATE TABLE IF NOT EXISTS tickers_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(50),
    price NUMERIC(10, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da materialized view 'ohlcv_daily'
CREATE MATERIALIZED VIEW IF NOT EXISTS ohlcv_daily AS
SELECT ticker, date_trunc('day', timestamp) as day, 
       MIN(price) as open, MAX(price) as close, 
       MIN(price) as low, MAX(price) as high
FROM tickers_data
GROUP BY ticker, date_trunc('day', timestamp);
