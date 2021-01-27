import pandas as pd

#Market and trader objects from
from Classes import trader 

#stock market compoonent of trading model

#handles collecting order and processing selling / buying of stocks

bitData = pd.read_csv("Data/Bitcoin_Min_Jan20.csv")

tr = trader(50000, 0)

def getStockOrder (n, order, date, trader):
    infoAtDate = bitData.loc[bitData['time_period_start'] == date]
    
    #verify the col index****
    stockPrice = infoAtDate.iloc[0,8]
    print(str(stockPrice))
    
    #let order be value 1, 0, -1
    #let n be int for number of shares
    if order == 0:
        print("Trader is holding")
    if order == 1:
        print("Trader is buying")
        saleprice = n * stockPrice
        trader.bank = trader.bank - saleprice
        trader.portfolio = trader.portfolio + n
        print("Removing $" + str(saleprice) + " from bank")
        print("Adding " + str(n) + " shares to portfolio")
        print("Trader has $" + str(trader.bank) + " in bank")
        print("Trader has " + str(n) + " shares in portfolio")
    if order == -1:
        print("Trader is selling")
        saleprice = n * stockPrice
        trader.bank = trader.bank - saleprice
        trader.portfolio = trader.portfolio + n
        print("Adding $" + str(saleprice) + " to bank")
        print("Removing " + n + " shares from portfolio")

getStockOrder(1, 1, '2020-01-01T00:00:00.0000000Z', tr)