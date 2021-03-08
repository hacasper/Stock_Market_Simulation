import pandas as pd
import numpy as np
#Market and trader objects from
from Classes import trader, market

#stock market compoonent of trading model
dfBTC = pd.read_csv("Data/Bitcoin_Min_Jan20.csv")
dfETH = pd.read_csv("Data/Ether_Min_Jan20.csv")
dfLTC = pd.read_csv("Data/Lite_Min_Jan20.csv")
#handles collecting order and processing selling / buying of stocks
def Loader():
    #Data
    dfBTC = pd.read_csv("Data/Bitcoin_Min_Jan20.csv")
    dfETH = pd.read_csv("Data/Ether_Min_Jan20.csv")
    dfLTC = pd.read_csv("Data/Lite_Min_Jan20.csv")
    #biggest possible set using all datasets
    dim=min([dfBTC.shape[0],dfETH.shape[0],dfLTC.shape[0]])
    
    return dfBTC, dfETH, dfLTC, dim

def SetUp(dim,dfBTC, dfETH, dfLTC):
    buffer= 24*60*7 #1 Week data to use for models
    Lookback=75 #Amount of data that the Prediction Model Needs (60), but pass 75 
    # and then I only use 60 in the trader file itself
    horizon=dim-buffer #amount of timestamps in the for loop
    Hist = np.zeros([dim,3])
    PredHist = np.zeros([horizon,3])
    Hist[0:buffer,0] = np.array(dfBTC.iloc[0:buffer,8])
    Hist[0:buffer,1] = np.array(dfETH.iloc[0:buffer,8])
    Hist[0:buffer,2] = np.array(dfLTC.iloc[0:buffer,8])
    mBTC=market('BTC',dfBTC.iloc[buffer,1],dfBTC.iloc[buffer,8])
    mETH=market('ETH',dfETH.iloc[buffer,1],dfETH.iloc[buffer,8])
    mLTC=market('LTC',dfLTC.iloc[buffer,1],dfLTC.iloc[buffer,8])
    
    #Trader Variables
    RSP = 15
    g=np.zeros([horizon,3]) #current gain
    l=np.zeros([horizon,3]) #current loss
    RSIndex = np.zeros([horizon,3]) #current RSI

    
    return buffer,Lookback,horizon,Hist,PredHist,mBTC,mETH,mLTC,RSP,g,l,RSIndex
    

def getCurrentPrice(date, coin):
    if coin == 0:
        infoAtDate = dfBTC.iloc[date,:]
        btcPrice = infoAtDate.iloc[8]
        return btcPrice
    elif coin == 1:
        infoAtDate = dfETH.iloc[date,:]
        ethPrice = infoAtDate.iloc[8]
        return ethPrice
    elif coin == 2:
        infoAtDate = dfLTC.iloc[date,:]
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
        infoAtDate = dfBTC.iloc[date,:]
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
        infoAtDate = dfETH.iloc[date,:]
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
        infoAtDate = dfLTC.iloc[date,:]
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
        
def summarize(sumtable,trader1,trader2,trader3,trader4,trader5,trader6,trader7,trader8,trader9,trader10,t,Hist,cols2):
    s1=np.sum(trader1.portfolio*Hist)+trader1.bank
    s2=np.sum(trader2.portfolio*Hist)+trader2.bank
    s3=np.sum(trader3.portfolio*Hist)+trader3.bank
    s4=np.sum(trader4.portfolio*Hist)+trader4.bank
    s5=np.sum(trader5.portfolio*Hist)+trader5.bank
    s6=np.sum(trader6.portfolio*Hist)+trader6.bank
    s7=np.sum(trader7.portfolio*Hist)+trader7.bank
    s8=np.sum(trader8.portfolio*Hist)+trader8.bank
    s9=np.sum(trader9.portfolio*Hist)+trader9.bank
    s10=np.sum(trader10.portfolio*Hist)+trader10.bank
    sumrow = [t, s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]
    sumrowdf=pd.DataFrame([sumrow], columns=cols2)
    sumtable.table=pd.concat([sumtable.table, sumrowdf])

def difference(Sum,difftable,cols3):
    diffrow = np.array((Sum.table.iloc[-1,1:Sum.table.shape[1]])-(Sum.table.iloc[0,1:Sum.table.shape[1]]))
    diffrowdf=pd.DataFrame([diffrow], columns=cols3)
    difftable.table=pd.concat([difftable.table, diffrowdf])

