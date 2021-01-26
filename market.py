import pandas as pd

#Market and trader objects from
from Classes import trader 
from Classes import market

#stock market compoonent of trading model

#handles collecting order and processing selling / buying of stocks

bitData = pd.read_csv("Bitcoin_Min_Jan20.csv")

def getStockOrder (n, order, date):
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
        print("Removing $" + str(saleprice) + " from bank")
        print("Adding " + str(n) + " shares to portfolio")
    if order == -1:
        print("Trader is selling")
        saleprice = n * stockPrice
        print("Adding $" + str(saleprice) + " to bank")
        print("Removing " + n + " shares from portfolio")

getStockOrder(1, 1, '2020-01-01T00:00:00.0000000Z')