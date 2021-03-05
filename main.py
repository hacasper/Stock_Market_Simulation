#%%

import pandas as pd
import datetime as dt
import csv  
import numpy as np
import matplotlib.pyplot as plt
#from tensorflow.keras.models import load_model

from Classes import market, trader, summary
from trader import RuleTrader, SmartTrader, TieredTrader, HillTrade, JackTrader, LTrader, RandTrader
#m16 = load_model("PredModels/model16")

#from preds import PredB, PredE, PredL
from market import executeOrder, summarize, difference
from plotting import  Plotter, Analyze
from test_trader import makeOrder

dfBTC = pd.read_csv ("Data/Bitcoin_Min_Jan20.csv")
dfETH = pd.read_csv ("Data/Ether_Min_Jan20.csv")
dfLTC = pd.read_csv ("Data/Lite_Min_Jan20.csv")
#df = pd.read_csv ("Data/Ether_Min_Jan20.csv")
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
#initializing traders for testing
RSI_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0]) 
Adv_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
Hill_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
Jack_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
Tiered_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
Loser_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
Random_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])

#initializing dataframes to store transactions
cols = ["time", "Trader", "BTC", "ETH", "LTC", "bank", "bit_trade", "eth_trade", "lite_trade"]
RSI_Trader.transactions = pd.DataFrame(columns=cols)
Adv_Trader.transactions = pd.DataFrame(columns=cols)
Hill_Trader.transactions = pd.DataFrame(columns=cols)
Jack_Trader.transactions = pd.DataFrame(columns=cols)
Tiered_Trader.transactions = pd.DataFrame(columns=cols)
Loser_Trader.transactions = pd.DataFrame(columns=cols)
Random_Trader.transactions = pd.DataFrame(columns=cols)
#initializing summary table for all traders
cols2 = ['t', 'RSI_Total','Adv_Total','Hill_Total','Jack_Total','Tiered_Total','Loser_Total', 'Random_Total']
Sum=summary([])
Sum.table= pd.DataFrame(columns=cols2)

#initializing difference table for all traders
cols3 = ['RSI_Earnings','Adv_Earnings','Hill_Earnings','Jack_Earnings','Tiered_Earnings','Loser_Earnings','Random_Earnings']
Diff=summary([])
Diff.table=pd.DataFrame(columns=cols3)

def main():
    for t in range (buffer, buffer + 10):
        #indices: 10=trades, 9=volume, 8=close, 7=low, 6=high, 5=open, 1 time open
             
        #History Arrays
        Hist[t,0]=np.array(dfBTC.iloc[t,8])
        Hist[t,1]=np.array(dfETH.iloc[t,8])
        Hist[t,2]=np.array(dfLTC.iloc[t,8])
        
        
        #trader 1: only RSI LIONEL
        l[t-buffer,:], g[t-buffer,:], RSIndex[t-buffer,:], qty = RuleTrader(Hist[t-Lookback:t+1,:], RSP,g[t-buffer-1,:],l[t-buffer-1,:],RSIndex[t-buffer-1,:],RSI_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, RSI_Trader)
        transactionrow = [t, "RSI_Trader", RSI_Trader.portfolio[0], RSI_Trader.portfolio[1], RSI_Trader.portfolio[2], RSI_Trader.bank, RSI_Trader.order[0], RSI_Trader.order[1], RSI_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        RSI_Trader.transactions = pd.concat([RSI_Trader.transactions, transactionrow_df])
        
        #trader 2: Adv. Trader (Lionel)
        PredHist[t-buffer,:], qty = SmartTrader(Hist[t-Lookback:t+1,:], RSIndex[t-buffer,:], PredHist[t-buffer-10:t-buffer-2,:], Adv_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Adv_Trader)
        transactionrow = [t, "Adv_Trader", Adv_Trader.portfolio[0], Adv_Trader.portfolio[1], Adv_Trader.portfolio[2], Adv_Trader.bank, Adv_Trader.order[0], Adv_Trader.order[1], Adv_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Adv_Trader.transactions = pd.concat([Adv_Trader.transactions, transactionrow_df])
        
        #trader 3: 3 times up: sell, 3 times down: buy
        qty = HillTrade(Hist[t-5:t+1,:],Hill_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Hill_Trader)
        transactionrow = [t, "Hill_Trader", Hill_Trader.portfolio[0], Hill_Trader.portfolio[1], Hill_Trader.portfolio[2], Hill_Trader.bank, Hill_Trader.order[0], Hill_Trader.order[1], Hill_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Hill_Trader.transactions = pd.concat([Hill_Trader.transactions, transactionrow_df])

        #trader 4: Variable Risk Trader
        qty = JackTrader(Hist[t-Lookback:t+1,:],RSIndex[t-buffer,:],Jack_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Jack_Trader)
        transactionrow = [t, "Jack_Trader", Jack_Trader.portfolio[0], Jack_Trader.portfolio[1], Jack_Trader.portfolio[2], Jack_Trader.bank, Jack_Trader.order[0], Jack_Trader.order[1], Jack_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Jack_Trader.transactions = pd.concat([Jack_Trader.transactions, transactionrow_df])
        
        #Tiered RSI trader
        qty = TieredTrader(Hist[t-Lookback:t+1,:], RSIndex[t-buffer,:], Tiered_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Tiered_Trader)
        transactionrow = [t, "Tiered_Trader", Tiered_Trader.portfolio[0], Tiered_Trader.portfolio[1], Tiered_Trader.portfolio[2], Tiered_Trader.bank, Tiered_Trader.order[0], Tiered_Trader.order[1], Tiered_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Tiered_Trader.transactions = pd.concat([Tiered_Trader.transactions, transactionrow_df])

        #LoserTrader
        qty = LTrader(Hist[t-5:t+1,:],Loser_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Loser_Trader)
        transactionrow = [t, "Loser_Trader", Loser_Trader.portfolio[0], Loser_Trader.portfolio[1], Loser_Trader.portfolio[2], Loser_Trader.bank, Loser_Trader.order[0], Loser_Trader.order[1], Loser_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Loser_Trader.transactions = pd.concat([Loser_Trader.transactions, transactionrow_df])
        
        #RandomTrader
        qty = RandTrader(Hist[t-5:t+1,:], Random_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Random_Trader)
        transactionrow = [t, "Random_Trader", Random_Trader.portfolio[0], Random_Trader.portfolio[1], Random_Trader.portfolio[2], Random_Trader.bank, Random_Trader.order[0], Random_Trader.order[1], Random_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Random_Trader.transactions = pd.concat([Random_Trader.transactions, transactionrow_df])

        summarize(Sum,RSI_Trader,Adv_Trader,Hill_Trader,Jack_Trader,Tiered_Trader,Loser_Trader,Random_Trader,t,Hist[t,:],cols2)

    difference(Sum,Diff,cols3)

if __name__ == "__main__":
    main()
    print(RSI_Trader.transactions)
    print(Adv_Trader.transactions)
    print(Hill_Trader.transactions)
    print(Jack_Trader.transactions)
    print(Tiered_Trader.transactions)
    print(Loser_Trader.transactions)
    print(Random_Trader.transactions)
    print(Sum.table)
    print(Diff.table)
    Sum.table.to_csv('summary.csv')

#%%a


# Some Plots and Stuf
# Plotter(Sum,buffer,dfBTC,dfETH,dfLTC,RSI_Trader,Adv_Trader,Hill_Trader,Jack_Trader,Tiered_Trader,Loser_Trader,Random_Trader)
'''

'''

'''
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
'''





#Total Worth: 
    
# RT=np.sum(RSI_Trader.portfolio*Hist[buffer+np.shape(RSI_Trader.transactions)[0]-1,:])+RSI_Trader.bank
# AT=np.sum(Adv_Trader.portfolio*Hist[buffer+np.shape(Adv_Trader.transactions)[0]-1,:])+Adv_Trader.bank
# HT=np.sum(Hill_Trader.portfolio*Hist[buffer+np.shape(Hill_Trader.transactions)[0]-1,:])+Hill_Trader.bank
# JT=np.sum(Jack_Trader.portfolio*Hist[buffer+np.shape(Jack_Trader.transactions)[0]-1,:])+Jack_Trader.bank
# TT=np.sum(Tiered_Trader.portfolio*Hist[buffer+np.shape(Tiered_Trader.transactions)[0]-1,:])+Tiered_Trader.bank
# LT=np.sum(Loser_Trader.portfolio*Hist[buffer+np.shape(Loser_Trader.transactions)[0]-1,:])+Loser_Trader.bank
# RT=np.sum(Random_Trader.portfolio*Hist[buffer+np.shape(Random_Trader.transactions)[0]-1,:])+Random_Trader.bank
# plt.plot(Mins[0:10000],PredHist[0:10000])
# plt.plot(Mins[0:10000],Hist[buffer:buffer+10000,0])
# plt.show()

# plt.plot(Mins[-10000:],PredHist[-10000:])
# plt.plot(Mins[-10000:],Hist[dim-10000:,0])
# plt.show()