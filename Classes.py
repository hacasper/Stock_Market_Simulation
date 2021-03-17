# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:26:39 2021

In this file, required classes are defined and their attributes specified
"""



class trader:
    #creates trader object with set bank value and portfolio value
    def __init__(self, bank, portfolio, order, transactions):
        self.bank = bank
        self.portfolio = portfolio
        #portfolio array: [BTC, ETH, LTC]
        #array will contain number of shares that trader has of each coin
        self.order = order
        #order array: [BTC, ETH, LTC]
        #1: buy, 0: hold, -1: sell
        self.transactions = transactions
        self.blocker = [0,0,0] #Required to block over-trading
        self.tradeworth = [0,0,0] #Trader's Memory
        #The rest is just used for analysis:
        self.totBuys=[]
        self.totSells=[]
        self.posSells=[]
        self.negSells=[]
        self.dif=[]
        self.tsell=[]
        self.tbuy=[]
        
class market:
    #creates market object which stores the date/time & price of a coin for 
    #each instance in the simulation
    def __init__(self, ticker, date, price):
        self.ticker = ticker
        self.date = date
        self.price = price
        #self.hist = [] 
        
    def market_description(self):
        return "price on " + self.date + "is $" + self.price
        
    #def getMarketPrice(self):
    #add market file here
        
class summary:
    #summary table was easiest to implement as a class with just a df in it.
    def __init__(self,DataFrame):
        self.table=DataFrame

