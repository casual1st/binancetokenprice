#!/usr/bin/python3
import requests
import pandas as pd
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_binance_data(symbol=None, interval='1m', limit=1):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return None

def print_binance_data(symbol, data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
                                     'quote_asset_volume', 'number_of_trades', 
                                     'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    print(f"\n{symbol} Data:")
    print(df[['timestamp', 'close']])

def process_symbol(symbol, interval):
    print(f"\nFetching current price for {symbol}...")
    data = fetch_binance_data(symbol, interval)
    if data:
        print("Current price:")
        print_binance_data(symbol, data)
    
    print(f"Waiting 10 minutes for {symbol}...")
    time.sleep(600)
    
    print(f"\nFetching price for {symbol} after 10 minutes...")
    data_10min = fetch_binance_data(symbol, interval)
    if data_10min:
        print("Price after 10 minutes:")
        print_binance_data(symbol, data_10min)
    
    print(f"Waiting 10 more minutes for {symbol}...")
    time.sleep(600)
    
    print(f"\nFetching price for {symbol} after 20 minutes...")
    data_20min = fetch_binance_data(symbol, interval)
    if data_20min:
        print("Price after 20 minutes:")
        print_binance_data(symbol, data_20min)

def main():
    pairs_input = input("Enter pairs as comma-separated values (BNBUSDT,ARBUSDT,ETHUSDT,BTCUSDT,SOLUSDT): ")
    pairs = [pair.strip() for pair in pairs_input.split(',')]

    interval = '1m'

    with ThreadPoolExecutor(max_workers=len(pairs)) as executor:
        executor.map(lambda pair: process_symbol(pair, interval), pairs)

if __name__ == "__main__":
    main()
