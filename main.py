#%%

import pandas as pd
import datetime as dt
import math
import pprint
import csv  
import numpy as np
import matplotlib.pyplot as plt
#from tensorflow.keras.models import load_model

from Classes import market, trader
from trader import StupidTrader, SmartTrader
#m16 = load_model("PredModels/model16")

#from preds import PredB, PredE, PredL
from market import executeOrder, getCurrentPrice
from test_trader import makeOrder

dfBTC = pd.read_csv ("Data/Bitcoin_Min_Jan20.csv")
dfETH = pd.read_csv ("Data/Ether_Min_Jan20.csv")
dfLTC = pd.read_csv ("Data/Lite_Min_Jan20.csv")
df = pd.read_csv ("Data/Ether_Min_Jan20.csv")
dim=min([dfBTC.shape[0],dfETH.shape[0],dfLTC.shape[0]])

#pd.concat([dfBTC,dfETH]).drop_duplicates(subset = Pr['col2'], keep=False)
#%%
buffer= 24*60*7 #1 Week data to use for models
Lookback=75 #Amount of data that the Prediction Model Needs (60)
horizon=dim-buffer #amount of timestamps in the for loop


#########################
"""
This plots stockdata for January 2021 for Bitcoin Data, illustrating areas of 
training and actual simulation.
base = dt.date(2020, 1, 1)
arr = list([base + dt.timedelta(weeks=i) for i in range(5)])
tik = list([-buffer, 0, buffer, 2*buffer, 3*buffer])

Mins=np.array(list(range(0,horizon)))
ng=np.array(list(range(-buffer,0)))
plt.title('Bitcoin Stockdata January 2020')
plt.plot(ng,dfBTC.iloc[0:buffer,8])
plt.plot(Mins,dfBTC.iloc[buffer:dim,8])
plt.legend(['Data used for Models and Trends','Data used for Simulation'])
plt.vlines(0,min(dfBTC.iloc[0:dim,8]),max(dfBTC.iloc[0:dim,8]),colors='k',linestyles='dashed')
plt.xticks(tik,arr)
plt.show()
"""
#########################

#Once we have models that work we either pull recent data and test  on that
#or we can just use only partial amounts of the datasets to calibrate and then test

Closing = np.zeros([horizon,1])
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
order = np.zeros([horizon,3,3]) #current order state

#%%
RSI_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0]) #Define Outside to keep data
Adv_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
cols = ["time", "Trader", "BTC", "ETH", "LTC", "bank", "bit_trade", "eth_trade", "lite_trade"]
RSI_Trader.transactions = pd.DataFrame(columns=cols)
Adv_Trader.transactions = pd.DataFrame(columns=cols)

def main():
    for t in range (buffer,buffer + 50):
        #indices: 10=trades, 9=volume, 8=close, 7=low, 6=high, 5=open, 1 time open
             
        #History Arrays
        Hist[t,0]=np.array(dfBTC.iloc[t,8])
        Hist[t,1]=np.array(dfETH.iloc[t,8])
        Hist[t,2]=np.array(dfLTC.iloc[t,8])
        #trader 1: only RSI LIONEL
        l[t-buffer,:], g[t-buffer,:], RSIndex[t-buffer,:], qty = StupidTrader(Hist[t-Lookback:t+1,:], RSP,g[t-buffer-1,:],l[t-buffer-1,:],RSIndex[t-buffer-1,:],RSI_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, RSI_Trader)
        transactionrow = [t, "RSI_Trader", RSI_Trader.portfolio[0], RSI_Trader.portfolio[1], RSI_Trader.portfolio[2], RSI_Trader.bank, RSI_Trader.order[0], RSI_Trader.order[1], RSI_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        RSI_Trader.transactions = pd.concat([RSI_Trader.transactions, transactionrow_df])
        # transactionrow = [t, "RSI_Trader", RSI_Trader.portfolio, RSI_Trader.bank, RSI_Trader.order]
        # RSI_Trader.transactions = np.vstack(transactions, transactionrow)
        
        #trader 2: Adv. Trader (Lionel)
        Preds, qty = SmartTrader(Hist[t-Lookback:t+1,:], RSIndex[t-buffer,:], Adv_Trader)
        PredHist[t-buffer,:]=Preds
        for i in range (0,3):
            executeOrder(qty[i], i, t, Adv_Trader)
        transactionrow = [t, "Adv_Trader", Adv_Trader.portfolio[0], Adv_Trader.portfolio[1], Adv_Trader.portfolio[2], Adv_Trader.bank, Adv_Trader.order[0], Adv_Trader.order[1], Adv_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Adv_Trader.transactions = pd.concat([Adv_Trader.transactions, transactionrow_df])
        #Aria's trader
        
        
        
        
        
        
        #Define your own trader
        
        #getStockOrder(n, order, date, trader)
        #get market price at time t
        #Current Market with opening timestamp: 
        m=market('ETH',df.iloc[t,1],df.iloc[t,5])
        Closing[t-buffer]=m.price
        
        
        #trader: using RSI and market price make trading decision
        
        #update trader's portfolio/bank value based on trading decision
        
        if t % 1000 == 0:
            print("market price for " + m.ticker + " on " + m.date + " is " + str(m.price))
            
        
        #order[t-buffer]=RSI_Trader.order[1]
if __name__ == "__main__":
    main()
    print(RSI_Trader.transactions)
    print(Adv_Trader.transactions)
    
#%%
# plt.plot(Mins[0:10000],PredHist[0:10000])
# plt.plot(Mins[0:10000],Hist[buffer:buffer+10000,0])
# plt.show()

# plt.plot(Mins[-10000:],PredHist[-10000:])
# plt.plot(Mins[-10000:],Hist[dim-10000:,0])
# plt.show()