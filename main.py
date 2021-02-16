#%%

import pandas as pd
import datetime as dt
import math
import pprint
import csv  
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

from Classes import market, trader
from trader import StupidTrader
m16 = load_model("PredModels/model16")
from preds import Pred16
from market import executeOrder, getCurrentPrice
from test_trader import makeOrder

dfBTC = pd.read_csv ("Data/Bitcoin_Min_Jan20.csv")
df = pd.read_csv ("Data/Ether_Min_Jan20.csv")
dim=df.shape[0]

#pd.concat([dfBTC,dfETH]).drop_duplicates(subset = Pr['col2'], keep=False)
#%%
buffer=24*60*7 #1 Week data to use for models
Lookback=75 #Amount of data that the Prediction Model Needs
horizon=dim-buffer #amount of timestamps in the for loop


#########################
base = dt.date(2020, 1, 1)
arr = list([base + dt.timedelta(weeks=i) for i in range(5)])
tik = list([-buffer, 0, buffer, 2*buffer, 3*buffer])

Mins=np.array(list(range(0,horizon)))
ng=np.array(list(range(-buffer,0)))
plt.title('Etherum Stockdata January 2020')
plt.plot(ng,df.iloc[0:buffer,8])
plt.plot(Mins,df.iloc[buffer:dim,8])
plt.legend(['Data used for Models and Trends','Data used for Simulation'])
plt.vlines(0,min(df.iloc[0:dim,8]),max(df.iloc[0:dim,8]),colors='k',linestyles='dashed')
plt.xticks(tik,arr)
plt.show()
#########################

#Once we have models that work we either pull recent data and test  on that
#or we can just use only partial amounts of the datasets to calibrate and then test

Closing = np.zeros([horizon,1])
Hist = np.zeros([dim,4])
PredHist = np.zeros([horizon,1])
Hist[0:buffer-1,:] = np.array(df.iloc[0:buffer-1,5:9])
m=market('ETH',df.iloc[buffer-1,1],df.iloc[buffer-1,5])


#Trader Variables
RSP = 15
g=np.zeros([horizon,1]) #current gain
l=np.zeros([horizon,1]) #current loss
RSIndex = np.zeros([horizon,1]) #current RSI
order = np.zeros([horizon,1]) #current order state

#%%
transactions = np.array["time", "Trader", "portfolio", "bank", "trade"]
RSI_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0]) #Define Outside to keep data
def main():
    for t in range (buffer,buffer + 10000):
        #indices: 10=trades, 9=volume, 8=close, 7=low, 6=high, 5=open, 1 time open


        current_date = df.iloc[t,1]
        current_price = getCurrentPrice(t,1)
        
        #est_trader
        # test = trader(400000, [0,0,0], [0,0,0])
        # test.order[t-buffer] = makeOrder(current_price, test)
        # getStockOrder(1,1, current_date, test)
        
        #trader 1: only RSI LIONEL
        Hist[t,:]=np.array(df.iloc[t,5:9])
        l[t-buffer], g[t-buffer], RSIndex[t-buffer], qty = StupidTrader(Hist[t-Lookback:t+1,:], RSP,t,g[t-buffer-1],l[t-buffer-1],RSIndex[t-buffer-1],RSI_Trader,1)
        executeOrder(qty, 1, t, RSI_Trader)

        transactionrow = [t, "RSI_Trader", RSI_Trader.portfolio, RSI_Trader.bank, RSI_Trader.order]
        RSI_Trader.transactions = np.vstack(transactions, transactionrow)
        #Aria's trader

        #Define your own trader

        #getStockOrder(n, order, date, trader)
        #get market price at time t
        #Current Market with opening timestamp: 
        m=market('ETH',df.iloc[t,1],df.iloc[t,5])
        Closing[t-buffer]=m.price
        #prediction
        #output will be average price in 5 minutes
        #predi =  Pred16(Hist[:,0],m16,t)      
        #PredHist[t-buffer]=predi
        #get RSI from RSICalculator.py

        #trader: using RSI and market price make trading decision

        #update trader's portfolio/bank value based on trading decision
        
        if t % 1000 == 0:
            print("market price for " + m.ticker + " on " + m.date + " is " + str(m.price))
            
        
        order[t-buffer]=RSI_Trader.order[1]
if __name__ == "__main__":
    main()
    pprint(RSI_Trader.transactions)
#%%
# plt.plot(Mins[0:10000],PredHist[0:10000])
# plt.plot(Mins[0:10000],Hist[buffer:buffer+10000,0])
# plt.show()

# plt.plot(Mins[-10000:],PredHist[-10000:])
# plt.plot(Mins[-10000:],Hist[dim-10000:,0])
# plt.show()