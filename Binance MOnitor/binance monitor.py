import csv
from binance.client import Client
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Insira suas chaves API da Binance
API_KEY = "XXXX"
API_SECRET  = "XXX"

# Inicialize o cliente Binance
client = Client(API_KEY, API_SECRET)


def fetch_trade_history(symbol, start_date, end_date):
    """
    Obtém o histórico de trades para o par especificado.
    """
    trades = client.get_klines(symbol=symbol, startTime=start_date, endTime=end_date, interval=Client.KLINE_INTERVAL_1DAY)
    return trades

def get_all_usdt_pairs():
    """
    Retorna uma lista de todos os pares de trading que incluem USDT.
    """
    exchange_info = client.get_exchange_info()
    usdt_pairs = [symbol['symbol'] for symbol in exchange_info['symbols'] if 'USDT' in symbol['symbol'] and symbol['status'] == 'TRADING']
    return usdt_pairs

def process_trades(trades):
    """
    Converte os trades para um DataFrame e calcula os retornos diários.
    """
    data = []
    for trade in trades:
        data.append({
            "time": datetime.fromtimestamp(trade['time'] / 1000),
            "symbol": trade['symbol'],
            "side": "BUY" if trade['isBuyer'] else "SELL",
            "price": float(trade['price']),
            "quantity": float(trade['qty']),
            "quote_quantity": float(trade['quoteQty']),
        })
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time']).dt.date
    return df

def calculate_daily_returns(df):
    """
    Calcula os retornos diários de um DataFrame de trades.
    """
    df['value'] = df['price'] * df['quantity']
    daily_returns = df.groupby('time')['value'].sum().pct_change().dropna()
    return daily_returns

def plot_return_distribution(daily_returns):
    """
    Plota a distribuição dos retornos diários.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(daily_returns, bins=50, edgecolor='black', alpha=0.7)
    plt.title('Distribuição de Retornos Diários')
    plt.xlabel('Retorno Diário (%)')
    plt.ylabel('Frequência')
    plt.show()

def calculate_portfolio_metrics(daily_returns):
    """
    Calcula métricas de avaliação de carteira.
    """
    mean_return = daily_returns.mean()
    volatility = daily_returns.std()
    sharpe_ratio = mean_return / volatility if volatility != 0 else 0
    max_drawdown = (daily_returns.cumsum() - daily_returns.cumsum().cummax()).min()
    
    return {
        "Média de Retornos Diários": mean_return,
        "Volatilidade": volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Máximo Drawdown": max_drawdown
    }

def main():
    # Definir período dos últimos 12 meses
    end_date = datetime.utcnow()- timedelta(days=1)
    start_date = end_date - timedelta(days=30)
    try:
        account_info = client.get_account()
        print("Conexão com a API bem-sucedida!")
    except Exception as e:
        print(f"Erro de conexão com a API: {e}")


    # Converta datas para timestamps
    start_timestamp = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)
    print(f"start_timestamp: {start_timestamp}, end_timestamp: {end_timestamp}")
    print(f"Obtendo dados de trades de {start_date.date()} até {end_date.date()}...")

    # Obter pares com USDT
    usdt_pairs = get_all_usdt_pairs()
    print(f"Encontrados {len(usdt_pairs)} pares com USDT.")

    all_daily_returns = []

    for symbol in usdt_pairs:
        print(f"Processando trades para {symbol}...")
        try:
            trades = fetch_trade_history(symbol, start_timestamp, end_timestamp)
            if trades:
                df_trades = process_trades(trades)
                daily_returns = calculate_daily_returns(df_trades)
                all_daily_returns.append(daily_returns)
        except Exception as e:
            print(f"Erro ao processar {symbol}: {e}")

    # Combinar todos os retornos diários em um único DataFrame
    if all_daily_returns:
        combined_returns = pd.concat(all_daily_returns, axis=0)
        combined_returns = combined_returns.sort_index()

        # Plotar distribuição
        plot_return_distribution(combined_returns)

        # Calcular métricas
        metrics = calculate_portfolio_metrics(combined_returns)
        print("Métricas de Avaliação da Carteira:")
        for key, value in metrics.items():
            print(f"{key}: {value:.6f}")
    else:
        print("Nenhum trade encontrado para o período especificado.")


if __name__ == "__main__":
    main()
