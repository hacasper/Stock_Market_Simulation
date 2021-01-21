# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:26:39 2021

@author: nA
"""
import pandas as pd
import datetime
import math
import csv 


class trader:
    #creates trader object with set bank value and portfolio value
    def __init__(self, bank, portfolio):
        self.bank = bank
        self.portfolio = portfolio

class market:
    def __init__(self, ticker, date, price):
        self.ticker = ticker
        self.date = date
        self.price = price
    
    def market_description(self):
        return "price on " + self.date + "is $" + self.price

    def getMarketPrice(self):
        if(self.ticker == "AAPL") :
            with open ('AAPL_since2000_daily.csv') as stockdata:
                priceread = pd.read_csv(stockdata)
                
                return self.price