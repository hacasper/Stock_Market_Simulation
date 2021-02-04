import pandas as pd

#Market and trader objects from
from Classes import trader 

#stock market compoonent of trading model

#handles collecting order and processing selling / buying of stocks

btcData = pd.read_csv("Data/Bitcoin_Min_Jan20.csv")
ethData = pd.read_csv("Data/Ether_Min_Jan20.csv")


def getCurrentPrice(date, coin):
    if coin == 0:
        infoAtDate = btcData.iloc[date,:]
        btcPrice = infoAtDate.iloc[8]
        return btcPrice
    elif coin == 1:
        infoAtDate = ethData.iloc[date,:]
        ethPrice = infoAtDate.iloc[8]
        return ethPrice
    elif coin == 2:
        print("LITE data is coming...")
        return 100
    else:
        print("invalid coin key")
        return 0
def executeOrder (n, coin, date, trader): 

    #coin 0 : BTC
    #coin 1 : ETH
    #coin 2 : LTC
    if coin == 0:
        infoAtDate = btcData.iloc[date,:]
        stockPrice = infoAtDate.iloc[8]
        if trader.order[0] == 0:
            print("Trader is holding bitcoin")
        elif trader.order[0] == 1:
            print("Trader is buying bitcoin")
            saleprice = n * stockPrice
            trader.bank = trader.bank - saleprice
            trader.portfolio[0] = trader.portfolio[0] + n
            print("Removing $" + str(saleprice) + " from bank")
            print("Adding " + str(n) + " shares to portfolio")
            print("Trader has $" + str(trader.bank) + " in bank")
            print("Trader has " + str(n) + " shares in portfolio")
        elif trader.order[0]  == -1:
            print("Trader is selling")
            saleprice = n * stockPrice
            trader.bank = trader.bank + saleprice
            trader.portfolio[0] = trader.portfolio[0] - n
            print("Adding $" + str(saleprice) + " to bank")
            print("Removing " + str(n) + " shares from portfolio")
    elif coin == 1:
        infoAtDate = ethData.iloc[date,:]
        stockPrice = infoAtDate.iloc[8]
        if trader.order[1] == 0:
            print("Trader is holding ethereum")
        elif trader.order[1] == 1:
            print("Trader is buying ethereum")
            saleprice = n * stockPrice
            trader.bank = trader.bank - saleprice
            trader.portfolio[1] = trader.portfolio[1] + n
            print("Removing $" + str(saleprice) + " from bank")
            print("Adding " + str(n) + " shares to portfolio")
            print("Trader has $" + str(trader.bank) + " in bank")
            print("Trader has " + str(n) + " shares in portfolio")
        elif trader.order[1]  == -1:
            print("Trader is selling ethereum")
            saleprice = n * stockPrice
            trader.bank = trader.bank + saleprice
            trader.portfolio[1] = trader.portfolio[1] - n
            print("Adding $" + str(saleprice) + " to bank")
            print("Removing " + str(n) + " shares from portfolio")
    elif coin == 2:
        print("LITE data is coming...")
        

    


