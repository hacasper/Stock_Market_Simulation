#%%
'''
This file will run the Simulation and bring together all information in the 
for loop. 
'''
# Download Libraries (for list of dependencies, check README)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from trader import iniTrader, RuleTrader, SmartTrader, TieredTrader, HillTrade, JackTrader, LTrader, RandTrader, PredTrader, InsiderTrader, ShuffleTrader
from market import Loader, SetUp, executeOrder, summarize, difference
from plotting import  Plotter, Analyze
#%%
# Load Historical Stock data:
dfBTC, dfETH, dfLTC, dim = Loader()
#%%
# Define areas of training and testing and introduce arrays for simulation to save RAM 
buffer,Lookback,horizon,Hist,PredHist,mBTC,mETH,mLTC,RSP,g,l,RSIndex = SetUp(dim,dfBTC, dfETH, dfLTC)

#%%
#initializing traders for testing
RSI_Trader,Adv_Trader,Hill_Trader,Variable_Trader,Tiered_Trader,AntiRSI_Trader,Random_Trader,Pred_Trader,Insider_Trader,Shuffle_Trader,Sum,Diff,cols,cols2,cols3 = iniTrader('RSI_Trader','Adv_Trader','Hill_Trader','Variable_Trader','Tiered_Trader','AntiRSI_Trader','Random_Trader','Pred_Trader','Insider_Trader','Shuffle_Trader')

#%%
def main(): # Run the main Simulation
    for t in range (buffer, dim):

        #dfXYZ indices: 10=trades, 9=volume, 8=close, 7=low, 6=high, 5=open, 1 time open
        #History Arrays updated with new market price of time t
        Hist[t,0]=np.array(dfBTC.iloc[t,8])
        Hist[t,1]=np.array(dfETH.iloc[t,8])
        Hist[t,2]=np.array(dfLTC.iloc[t,8])
       
        
        #trader 1: RSI trader: Strategy solely based on RSI and certain thresholds
        l[t-buffer,:], g[t-buffer,:], RSIndex[t-buffer,:], qty = RuleTrader(Hist[t-Lookback:t+1,:], RSP,g[t-buffer-1,:],l[t-buffer-1,:],RSIndex[t-buffer-1,:],RSI_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, RSI_Trader)
        transactionrow = [t, "RSI_Trader", RSI_Trader.portfolio[0], RSI_Trader.portfolio[1], RSI_Trader.portfolio[2], RSI_Trader.bank, RSI_Trader.order[0], RSI_Trader.order[1], RSI_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        RSI_Trader.transactions = pd.concat([RSI_Trader.transactions, transactionrow_df])
       
        #trader 2: ADV trader: Combines Predictions, RSI and own approximations of momentum and trend reversals 
        PredHist[t-buffer,:], qty = SmartTrader(Hist[t-Lookback:t+1,:], RSIndex[t-buffer,:], PredHist[t-buffer-10:t-buffer-2,:], Adv_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Adv_Trader)
        transactionrow = [t, "Adv_Trader", Adv_Trader.portfolio[0], Adv_Trader.portfolio[1], Adv_Trader.portfolio[2], Adv_Trader.bank, Adv_Trader.order[0], Adv_Trader.order[1], Adv_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Adv_Trader.transactions = pd.concat([Adv_Trader.transactions, transactionrow_df])
       
        #trader 3: Hill trader: Whenever there is a hill, we trade ==> 3 up: buy, 3 down: sell (counterintuitive)
        qty = HillTrade(Hist[t-6:t+1,:],Hill_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Hill_Trader)
        transactionrow = [t, "Hill_Trader", Hill_Trader.portfolio[0], Hill_Trader.portfolio[1], Hill_Trader.portfolio[2], Hill_Trader.bank, Hill_Trader.order[0], Hill_Trader.order[1], Hill_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Hill_Trader.transactions = pd.concat([Hill_Trader.transactions, transactionrow_df])
 
        #trader 4: Variable Trader: Same as RSI but easily adjusted thresholds
        qty = JackTrader(Hist[t-Lookback:t+1,:],RSIndex[t-buffer,:],Variable_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Variable_Trader)
        transactionrow = [t, "Variable_Trader", Variable_Trader.portfolio[0], Variable_Trader.portfolio[1], Variable_Trader.portfolio[2], Variable_Trader.bank, Variable_Trader.order[0], Variable_Trader.order[1], Variable_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Variable_Trader.transactions = pd.concat([Variable_Trader.transactions, transactionrow_df])

        #trader 5: Tiered RSI Trader: Multiple levels of RSI to avoid thresholds, varying amounts
        qty = TieredTrader(Hist[t-Lookback:t+1,:], RSIndex[t-buffer,:], Tiered_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Tiered_Trader)
        transactionrow = [t, "Tiered_Trader", Tiered_Trader.portfolio[0], Tiered_Trader.portfolio[1], Tiered_Trader.portfolio[2], Tiered_Trader.bank, Tiered_Trader.order[0], Tiered_Trader.order[1], Tiered_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Tiered_Trader.transactions = pd.concat([Tiered_Trader.transactions, transactionrow_df])
 
        #trader 6: Anti RSI threshold trader, should lose money if the theories are correct
        qty = LTrader(Hist[t-5:t+1,:],RSIndex[t-buffer,:],AntiRSI_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, AntiRSI_Trader)
        transactionrow = [t, "AntiRSI_Trader", AntiRSI_Trader.portfolio[0], AntiRSI_Trader.portfolio[1], AntiRSI_Trader.portfolio[2], AntiRSI_Trader.bank, AntiRSI_Trader.order[0], AntiRSI_Trader.order[1], AntiRSI_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        AntiRSI_Trader.transactions = pd.concat([AntiRSI_Trader.transactions, transactionrow_df])

        #trader 7: Random Trader, randomly choses if buy, sell or hold and uses that decision
        qty = RandTrader(Hist[t-5:t+1,:], Random_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Random_Trader)
        transactionrow = [t, "Random_Trader", Random_Trader.portfolio[0], Random_Trader.portfolio[1], Random_Trader.portfolio[2], Random_Trader.bank, Random_Trader.order[0], Random_Trader.order[1], Random_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Random_Trader.transactions = pd.concat([Random_Trader.transactions, transactionrow_df])

       #trader 8: Prediction Trader, Heavily relies on his prediction algorithms to make trading decisions, less on other inputs
        qty = PredTrader(PredHist[t-buffer,:],Hist[t-Lookback:t+1,:], Pred_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Pred_Trader)
        transactionrow = [t, "Pred_Trader", Pred_Trader.portfolio[0], Pred_Trader.portfolio[1], Pred_Trader.portfolio[2], Pred_Trader.bank, Pred_Trader.order[0], Pred_Trader.order[1], Pred_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Pred_Trader.transactions = pd.concat([Pred_Trader.transactions, transactionrow_df])
       
        #trader 9: InsiderTrader, gets access about future stock prices, and with a certain likelyhood receives that info and uses it to trade
        if t<dim-1446:
            Insider=[np.mean(dfBTC.iloc[t+1440:t+1446,8]),np.mean(dfETH.iloc[t+1440:t+1446,8]),np.mean(dfLTC.iloc[t+1440:t+1446,8])]
        if t>=dim-1446:
            Insider=Hist[-1,:]
        qty = InsiderTrader(Hist[t-10:t+1,:], RSIndex[t-buffer,:], Insider, Insider_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Insider_Trader)
        transactionrow = [t, "Insider_Trader", Insider_Trader.portfolio[0], Insider_Trader.portfolio[1], Insider_Trader.portfolio[2], Insider_Trader.bank, Insider_Trader.order[0], Insider_Trader.order[1], Insider_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Insider_Trader.transactions = pd.concat([Insider_Trader.transactions, transactionrow_df])

        #trader 10: ShuffleTrader, can sell coins in order to do big buys of coins at good moments in time.
        qty = ShuffleTrader(Hist[t-Lookback:t+1,:],RSIndex[t-buffer,:],Shuffle_Trader)
        for i in range (0,3):
            executeOrder(qty[i], i, t, Shuffle_Trader)
        transactionrow = [t, "Shuffle_Trader", Shuffle_Trader.portfolio[0], Shuffle_Trader.portfolio[1], Shuffle_Trader.portfolio[2], Shuffle_Trader.bank, Shuffle_Trader.order[0], Shuffle_Trader.order[1], Shuffle_Trader.order[2]]
        transactionrow_df = pd.DataFrame([transactionrow], columns=cols)
        Shuffle_Trader.transactions = pd.concat([Shuffle_Trader.transactions, transactionrow_df])

        #Saves the trader data to a df for later analysis
        summarize(Sum,RSI_Trader,Adv_Trader,Hill_Trader,Variable_Trader,Tiered_Trader,AntiRSI_Trader,Random_Trader,Pred_Trader,Insider_Trader,Shuffle_Trader,t,Hist[t,:],cols2)

        if t%1000 == 0: #Receive Feedback every 10000 minutes
            print (Sum.table)
    #Calculate the final difference from end of simulation to beginning of simulation
    difference(Sum,Diff,cols3)


if __name__ == "__main__":
    main() #Print Transaction Tables, the Sum and Dif Tables
    print(RSI_Trader.transactions)
    print(Adv_Trader.transactions)
    print(Hill_Trader.transactions)
    print(Variable_Trader.transactions)
    print(Tiered_Trader.transactions)
    print(AntiRSI_Trader.transactions)
    print(Random_Trader.transactions)
    print(Shuffle_Trader.transactions)
    print(Sum.table)
    print(Diff.table)
    Sum.table.to_csv('summary.csv') #Save the table to csv

#%%
#Plot Data and save figures in figures folder
Plotter(Sum,buffer,dfBTC,dfETH,dfLTC,RSI_Trader,Adv_Trader,Hill_Trader,Variable_Trader,Tiered_Trader,AntiRSI_Trader,Random_Trader,Pred_Trader,Insider_Trader,Shuffle_Trader)
#%%
#Analyze Traders and save figures in figures folder
# Calculates Trade Balances and identifies buy / sell signals
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,RSI_Trader,'./Figures/RSI_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,Adv_Trader,'./Figures/Advanced_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,Hill_Trader,'./Figures/Momentum_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,Variable_Trader,'./Figures/Variable_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,Tiered_Trader,'./Figures/Tiered_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,AntiRSI_Trader,'./Figures/AntiRSI_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,Random_Trader,'./Figures/Random_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,Pred_Trader,'./Figures/Predictions_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,Insider_Trader,'./Figures/Insider_Trader.pdf')
Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,Shuffle_Trader,'./Figures/Extreme_Trader.pdf')

#%%
# Double Check Predicitons: These curves should overlap almost entirely!
plt.figure()
Mins=np.array(list(range(0,horizon)))
plt.plot(Mins[-10000:],PredHist[-10000:,0])
plt.plot(Mins[-10000:],Hist[dim-10000:,0])
plt.show()
# %%
