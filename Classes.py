# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:26:39 2021

@author: nA
"""
import pandas as pd
import datetime
import numpy as np
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
        #self.hist = [] 
    
    def market_description(self):
        return "price on " + self.date + "is $" + self.price

    #def getMarketPrice(self):
    #add market file here
            
class pred:
    def __init__(self,horizon):
        self.RSI=0
        self.p1=0
        self.p10=[0,0,0,0,0,0,0,0,0,0]
        self.p30=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.hist10=np.empty([horizon,10])
        self.hist100=np.empty(horizon,100)