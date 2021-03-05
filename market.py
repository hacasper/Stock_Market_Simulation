import pandas as pd
import numpy as np
#Market and trader objects from
from Classes import trader 

#stock market compoonent of trading model

#handles collecting order and processing selling / buying of stocks

btcData = pd.read_csv("Data/Bitcoin_Min_Jan20.csv")
ethData = pd.read_csv("Data/Ether_Min_Jan20.csv")
ltcData = pd.read_csv("Data/Lite_Min_Jan20.csv")

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
        infoAtDate = ltcData.iloc[date,:]
        ltcPrice = infoAtDate.iloc[8]
        return ltcPrice
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
            saleprice = 0
            #print("Trader is holding bitcoin")
        elif trader.order[0] == 1:
            #print("Trader is buying bitcoin")
            saleprice = n * stockPrice * 1.005
            if trader.bank < saleprice:
                trader.order[0] = 0
            else:
                trader.bank = trader.bank - saleprice
                trader.portfolio[0] = trader.portfolio[0] + n
            #print("Removing $" + str(saleprice) + " from bank")
            #print("Adding " + str(n) + " shares to portfolio")
            #print("Trader has $" + str(trader.bank) + " in bank")
            #print("Trader has " + str(n) + " shares in portfolio")
        elif trader.order[0]  == -1:
            #print("Trader is selling")
            saleprice = n * stockPrice * 0.995
            if trader.portfolio[0] > n:
                trader.bank = trader.bank + saleprice
                trader.portfolio[0] = trader.portfolio[0] - n
            else:
                trader.order[0] = 0
            #print("Adding $" + str(saleprice) + " to bank")
            #print("Removing " + str(n) + " shares from portfolio")

    elif coin == 1:
        infoAtDate = ethData.iloc[date,:]
        stockPrice = infoAtDate.iloc[8]
        if trader.order[1] == 0:
            saleprice = 0
            #print("Trader is holding ethereum")
        elif trader.order[1] == 1:
            #print("Trader is buying ethereum")
            saleprice = n * stockPrice * 1.005
            if trader.bank < saleprice:
                trader.order[1] = 0
            else:
                trader.bank = trader.bank - saleprice
                trader.portfolio[1] = trader.portfolio[1] + n
            #print("Removing $" + str(saleprice) + " from bank")
            #print("Adding " + str(n) + " shares to portfolio")
            #print("Trader has $" + str(trader.bank) + " in bank")
            #print("Trader has " + str(n) + " shares in portfolio")
        elif trader.order[1]  == -1:
            #print("Trader is selling ethereum")
            saleprice = n * stockPrice * 0.995
            if trader.portfolio[1] > n:
                trader.bank = trader.bank + saleprice
                trader.portfolio[1] = trader.portfolio[1] - n
            else:
                trader.order[1] = 0
            #print("Adding $" + str(saleprice) + " to bank")
            #print("Removing " + str(n) + " shares from portfolio")
            #print("Trader has $" + str(trader.bank) + " in bank")
            #print("Trader has " + str(n) + " shares in portfolio")
    elif coin == 2:
        infoAtDate = ltcData.iloc[date,:]
        stockPrice = infoAtDate.iloc[8]
        if trader.order[2] == 0:
            saleprice = 0
            #print("Trader is holding litecoin")
        elif trader.order[2] == 1:
            #print("Trader is buying litecoin")
            saleprice = n * stockPrice * 1.005
            if trader.bank < saleprice:
                trader.order[2] = 0
            else:
                trader.bank = trader.bank - saleprice
                trader.portfolio[2] = trader.portfolio[2] + n
            #print("Removing $" + str(saleprice) + " from bank")
            #print("Adding " + str(n) + " shares to portfolio")
            #print("Trader has $" + str(trader.bank) + " in bank")
            #print("Trader has " + str(n) + " shares in portfolio")
        elif trader.order[2]  == -1:
            #print("Trader is selling litecoin")
            saleprice = n * stockPrice * 0.995 
            if trader.portfolio[2] > n:
                trader.bank = trader.bank + saleprice
                trader.portfolio[2] = trader.portfolio[2] - n
            else:
                trader.order[2] = 0
            #print("Adding $" + str(saleprice) + " to bank")
            #print("Removing " + str(n) + " shares from portfolio")
            #print("Trader has $" + str(trader.bank) + " in bank")
            #print("Trader has " + str(n) + " shares in portfolio")
        
def summarize(sumtable,trader1,trader2,trader3,trader4,trader5,trader6,trader7,t,Hist,cols2):
    s1=np.sum(trader1.portfolio*Hist)+trader1.bank
    s2=np.sum(trader2.portfolio*Hist)+trader2.bank
    s3=np.sum(trader3.portfolio*Hist)+trader3.bank
    s4=np.sum(trader4.portfolio*Hist)+trader4.bank
    s5=np.sum(trader5.portfolio*Hist)+trader5.bank
    s6=np.sum(trader6.portfolio*Hist)+trader6.bank
    s7=np.sum(trader7.portfolio*Hist)+trader7.bank
    sumrow = [t, s1,s2,s3,s4,s5,s6,s7]
    sumrowdf=pd.DataFrame([sumrow], columns=cols2)
    sumtable.table=pd.concat([sumtable.table, sumrowdf])

def difference(Sum,difftable,cols3):
    diffrow = pd.to_numeric(Sum.table.iloc[-1,1:Sum.table.shape[1]])-pd.to_numeric(Sum.table.iloc[0,1:Sum.table.shape[1]])
    diffrowdf=pd.DataFrame([diffrow], columns=cols3, dtype=float)
    difftable.table=pd.to_numeric(pd.concat([difftable.table, diffrowdf]))

