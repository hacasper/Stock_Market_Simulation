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

    #still working
    def getMarketPrice(self):
        if(self.ticker == "AAPL") :
            with open ('AAPL_since2000_daily.csv') as stockdata:
                priceread = pd.read_csv(stockdata)
                return self.price
        if(self.ticker == "BIT"):
            with open('Bitcoin_Min_Jan20.csv') as stockdata:
                priceread = pd.read_csv(stockdata)
                price = 
                return self.priceq


def main():
    tr1 = trader(100000, "ETH")
    print("trader owns " + tr1.portfolio + " and $" + str(tr1.bank) + " left in the bank")

    m1 = market("AAPL", "1/19/2021", 100)
    print("market price for " + m1.ticker + " on " + m1.date + " is " + str(m1.price))

if __name__ == "__main__":
    main()
    