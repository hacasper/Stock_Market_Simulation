# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 12:40:15 2021

@author: saber
"""
import datetime as dt
import pandas as pd
import math
import csv  
import numpy as np
from datetime import timedelta

#from Classes import market
#from CLasses import trader
bank = 500
shares = 10
market_value = 1
rsi = 12

bank_1 = bank + (shares*market_value)
shares_1 = 0
bank_2 = bank + ((2*shares*market_value)/3)
shares_2 = shares - (bank*2)/(3*market_value)
bank_3 = bank + ((shares*market_value)/2)
shares_3 = shares - (bank/(2*market_value))
bank_4 = bank + ((shares*market_value)/4)
shares_4 = shares - (bank/4*market_value)
bank_5 = bank
shares_5 = shares 
bank_6 = bank
shares_6 = shares
bank_7 = bank - (bank/4)
shares_7 = shares + (bank/(4*market_value))
bank_8 = bank - (bank/2)
shares_8 = shares + (bank/(2*market_value))
bank_9 = bank - ((2*bank)/3)
shares_9 = shares + (bank*2)/(3*market_value)
bank_10 = 0
shares_10 = shares + (bank/market_value)


if rsi > 90:
    print("New Bank Amt:", bank_1)
    print("New Shares Amt: ", shares_1)
elif 90>rsi>80:
    print("New Bank Amt:", bank_2)
    print("New Shares Amt: ", shares_2)
elif 80>rsi>70:
    print("New Bank Amt:", bank_3)
    print("New Shares Amt: ", shares_3)
elif 70>rsi>60:
    print("New Bank Amt:", bank_4)
    print("New Shares Amt: ", shares_4)
elif 60>rsi>50:
    print("New Bank Amt:", bank_5)
    print("New Shares Amt: ", shares_5)
elif 50>rsi>40:
    print("New Bank Amt:", bank_6)
    print("New Shares Amt: ", shares_6)
elif 40>rsi>30:
    print("New Bank Amt:", bank_7)
    print("New Shares Amt: ", shares_7)
elif 30>rsi>20:
    print("New Bank Amt:", bank_8)
    print("New Shares Amt: ", shares_8)
elif 20>rsi>10:
    print("New Bank Amt:", bank_9)
    print("New Shares Amt: ", shares_9)
elif 10>rsi>0:
    print("New Bank Amt:", bank_10)
    print("New Shares Amt: ", shares_10)
else:
    print("error")