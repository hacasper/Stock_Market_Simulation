# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 17:49:57 2021

@author: Lionel Hanke
"""

import os
import requests
import pandas as pd
import numpy as np
import json
import datetime as dt
import matplotlib.pyplot as plt

import config


MyKey=config.api_key

API_KEY = os.environ.get('COINAPI_KEY', MyKey)
headers = {
    'X-CoinAPI-Key': API_KEY
}





#See what periods are Available
#resp = requests.get(
#    f'https://rest.coinapi.io/v1/ohlcv/periods',
#    headers=headers)

#See what Exchanges we can use
#resp = requests.get(
#    f'https://rest.coinapi.io/v1/exchanges/Coinbase',
#    headers=headers)
#Coinbase chosen arbitrarily

#Check whether Coinbase has the symbols we want
#resp = requests.get(
#    f'https://rest.coinapi.io/v1/symbols?filter_symbol_id=SPOT_ETH_USD',
#    headers=headers)

#Request OHLC data from coinAPI.io for BTC, ETH
# in the past 3 years (minute data and daily data)
#Bitcoin

#"symbol_id": "COINBASE_SPOT_BTC_USD",\n    "exchange_id": "COINBASE",\n    "symbol_type": "SPOT",\n    "asset_id_base": "BTC",\n    "asset_id_quote": "USD",\n    "data_start": "2015-01-14",\n    "data_end": "2021-01-20",
#"symbol_id": "BINANCE_SPOT_BTC_USDT",\n    "exchange_id": "BINANCE",\n    "symbol_type": "SPOT",\n    "asset_id_base": "BTC",\n    "asset_id_quote": "USDT",\n    "data_start": "2017-08-17",\n    "data_end": "2021-01-20",\n   
# "symbol_id": "COINBASE_SPOT_ETH_USD",\n    "exchange_id": "COINBASE",\n    "symbol_type": "SPOT",\n    "asset_id_base": "ETH",\n    "asset_id_quote": "USD",\n    "data_start": "2016-06-09",\n    "data_end": "2021-01-20"
#"symbol_id": "BINANCE_SPOT_ETH_USDT",\n    "exchange_id": "BINANCE",\n    "symbol_type": "SPOT",\n    "asset_id_base": "ETH",\n    "asset_id_quote": "USDT",\n    "data_start": "2017-08-17",\n    "data_end": "2021-01-20"

#BTC
# symbol_id = 'COINBASE_SPOT_BTC_USD'
# #symbol_id = 'COINBASE_SPOT_ETH_USD'
# period_id = '1MIN'
# time_start = '2018-01-01'
# time_end ='2021-01-01'
# limit = 100000



#Get Bitcoin Minute data for January 2020
# respBTC = requests.get('https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_BTC_USD/history?period_id=1MIN&time_start=2020-01-01&time_end=2020-02-01&limit=100000&include_empty_items=1',headers=headers)

# data_BTC = pd.read_json(respBTC.text)
# data_BTC.to_csv('Bitcoin_Min_Jan20.csv')


#Get Ether Minute data for January 2018
respETH = requests.get('https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_ETH_USD/history?period_id=1MIN&time_start=2020-01-01&time_end=2020-02-01&limit=100000&include_empty_items=1',headers=headers)

data_ETH = pd.read_json(respETH.text)
data_ETH.to_csv('Ether_Min_Jan20.csv')


#Get Bitcoin daily data 2018-2021
respBTCd = requests.get('https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_BTC_USD/history?period_id=1DAY&time_start=2018-01-01&time_end=2021-01-01&limit=100000&include_empty_items=1',headers=headers)

data_BTCd = pd.read_json(respBTCd.text)
data_BTCd.to_csv('Bitcoin_Day_1820.csv')

#Get Ether daily data 2018-2021
respETHd = requests.get('https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_ETH_USD/history?period_id=1DAY&time_start=2018-01-01&time_end=2021-01-01&limit=100000&include_empty_items=1',headers=headers)

data_ETHd = pd.read_json(respETHd.text)
data_ETHd.to_csv('Ether_Day_1820.csv')


#Get Bitcoin hourly data 2018-2021
respBTCh = requests.get('https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_BTC_USD/history?period_id=1HOUR&time_start=2018-01-01&time_end=2021-01-01&limit=100000&include_empty_items=1',headers=headers)

data_BTCh = pd.read_json(respBTCh.text)
data_BTCh.to_csv('Bitcoin_Hour_1820.csv')


#Get Ether hourly data 2018-2021
respETHh = requests.get('https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_ETH_USD/history?period_id=1HOUR&time_start=2018-01-01&time_end=2021-01-01&limit=100000&include_empty_items=1',headers=headers)

data_ETHh = pd.read_json(respETHh.text)
data_ETHh.to_csv('Ether_Hour_1820.csv')

