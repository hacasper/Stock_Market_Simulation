# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 13:42:26 2021

@author: Lionel
This file stores all trader logics, the initialize functions and the RSI 
calculations
"""
#Libraries and Dependencies
from preds import PredB, PredE, PredL
import numpy as np
import math
import random
import pandas as pd
from Classes import trader, summary

#Initialize traders
def iniTrader(RSI_Trader,Adv_Trader,Hill_Trader,Variable_Trader,Tiered_Trader,AntiRSI_Trader,Random_Trader,Pred_Trader,Insider_Trader,Shuffle_Trader):
    RSI_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    Adv_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    Hill_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    Variable_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    Tiered_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    AntiRSI_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    Random_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    Pred_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    Insider_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    Shuffle_Trader = trader(400000, [0,0,0], [0,0,0], [0, 0, 0, 0])
    
    cols = ["time", "Trader", "BTC", "ETH", "LTC", "bank", "bit_trade", "eth_trade", "lite_trade"]
    RSI_Trader.transactions = pd.DataFrame(columns=cols)
    Adv_Trader.transactions = pd.DataFrame(columns=cols)
    Hill_Trader.transactions = pd.DataFrame(columns=cols)
    Variable_Trader.transactions = pd.DataFrame(columns=cols)
    Tiered_Trader.transactions = pd.DataFrame(columns=cols)
    AntiRSI_Trader.transactions = pd.DataFrame(columns=cols)
    Random_Trader.transactions = pd.DataFrame(columns=cols)
    Insider_Trader.transactions = pd.DataFrame(columns=cols)
    Pred_Trader.transactions = pd.DataFrame(columns=cols)
    Shuffle_Trader.transactions = pd.DataFrame(columns=cols)
    
    cols2 = ['t', 'RSI_Total','Adv_Total','Hill_Total','Jack_Total','Tiered_Total','Loser_Total', 'Random_Total','Pred_Total','Insider_Total','Shuffle_Total']
    Sum=summary([])
    Sum.table= pd.DataFrame(columns=cols2)
    #initializing difference table for all traders
    cols3 = ['RSI_Earnings','Adv_Earnings','Hill_Earnings','Jack_Earnings','Tiered_Earnings','Loser_Earnings','Random_Earnings','Pred_Earnings','Insider_Earnings','Shuffle_Earnings']
    Diff=summary([])
    Diff.table=pd.DataFrame(columns=cols3)
    return RSI_Trader,Adv_Trader,Hill_Trader,Variable_Trader,Tiered_Trader,AntiRSI_Trader,Random_Trader,Pred_Trader,Insider_Trader,Shuffle_Trader,Sum,Diff,cols,cols2,cols3

#This function calculates the RSI, either from an RSI and new prices or from
#an array of prices only (in order to Iitialize RSI)
def RSIblind(Hist,RSP,gain,loss,RSI):
    Lookback=int(60)
    rs=[0,0,0]
    rsind=[0,0,0]
    if RSI[0] == RSI[1] == RSI[2] == 0: #Initialize RSI, if none has been calculated yet
        val=Hist[-RSP:,:] #Catch relevant data from history
        var1=np.diff(val,axis=0) #Calculate the subsequent differences in the data
        dim=var1.shape[0]
        for j in range(0,3): #Loop over 3 Coins
            gain[j] = 0.000001
            loss[j] = 0.000001 #avoid division by zero
            for i in range(0,dim-1): #Loop over RSP
                if var1[i,j]>0:
                    gain[j] = gain[j] + var1[i,j] #add gains
                else:
                    loss[j] = loss[j] - var1[i,j] #add losses
            rs[j] = gain[j]/loss[j] #calculate RS for all coins
            gain[j]=gain[j]/14
            loss[j]=loss[j]/14
            rsind[j] = 100-(100/(1+rs[j]))
        return gain, loss, rsind #Return 3*(gain, loss, rsind) for the 3 coins
    else: #If RSI !=0, we only need to update, not do the whole initialization calculation:
        val=Hist[-RSP:,:]
        var1=np.diff(val,axis=0)#Returns vector of 14 diff, we only need the most recent one
        for j in range(0,3):
            if var1[-1,j] > 0:#if current dif positive
                cg = var1[-1,j] #then add this to the current gain
                cl = 0 #which means current loss is 0
            else:
                cl = -var1[-1,j]#if current dif negative, add loss to current loss
                cg = 0 #then the gain is 0
            gain[j] = (gain[j]*(RSP-2)+cg)/14 #now update gain and loss, calc RSI
            loss[j] = (loss[j]*(RSP-2)+cl)/14  
            rsind[j] = 100-(100/(1+(gain[j])/(loss[j])))       
        return gain, loss, rsind
        
    
def RuleTrader(Hist,RSP,gain,loss,RSI,trader):
    Lookback=int(60)
    fac=0.2 #What percentage of the bank should trader spend when he buys coins
    THIRDworth=(np.sum(trader.portfolio*Hist[-1,:])+trader.bank)/3
    #How much should be in a certain coin, if we divide total trader value by 3?
    maxPortfolio=THIRDworth/Hist[-1,:]
    gain, loss, rsindex = RSIblind(Hist,RSP,gain,loss,RSI) #calculate RSI
    # Only this trader calculates RSI, he then passes it to the main file, where
    # other traders can access the information (avoid multiple calc of same thing)
    amount=[0,0,0]
    for j in range (0,3):
        if rsindex[j] > 75 and trader.blocker[j]<=0: #Trade Rule: blocker needs to
        #be inactive (no trades in the past xy minutes) and RSI > 75 to sell
            trader.order[j] = -1
            amount[j] = np.floor(trader.portfolio[j]*10)/10 #Sell everything from that coin
            trader.blocker[j]=60
        elif 27 < rsindex[j] < 75: #Do nothing if we are in the middle region
            trader.order[j] = 0
            amount[j] = 0
            trader.blocker[j]=trader.blocker[j]-1 #But make sure the blocker goes down
        elif rsindex[j] < 27 and trader.blocker[j]<=0:
            trader.order[j] = 1
            amount[j] = np.floor(fac*(maxPortfolio[j]-trader.portfolio[j])*10)/10
            trader.blocker[j]=40
        if amount[j]==0: #Because of np.floor there is a possibility of amount =0,
        #although order !=0... Therefore: Just switch that back if it happens:
            trader.order[j]=0
            trader.blocker[j]=trader.blocker[j]-1
    return loss,gain,rsindex,amount
    
def TieredTrader(Hist,rsindex,trader):
    #Lookback=75
    amount=[0,0,0]
    for coin in range (0,3):
        if 100 > rsindex[coin] >= 90 and trader.blocker[coin]<=0: 
            trader.order[coin] = -1
            amount[coin] = trader.portfolio[coin]
            trader.blocker[coin]=30 
        #if RSI > 70 and order == 1:
            #order = 0
        elif 90 > rsindex[coin] >= 80 and trader.blocker[coin]<=0:
            trader.order[coin] = -1
            amount[coin] = (2/3)*trader.portfolio[coin]
            trader.blocker[coin]=30
        elif 80 > rsindex[coin] >= 70 and trader.blocker[coin]<=0: 
            trader.order[coin] = -1
            amount[coin] = (1/2)*trader.portfolio[coin]
            trader.blocker[coin]=30
        elif 70 > rsindex[coin] >= 60 and trader.blocker[coin]<=0:
            trader.order[coin] = -1
            amount[coin] = (1/4)*trader.portfolio[coin]
            trader.blocker[coin]=30
        elif 60 > rsindex[coin] >= 50:
            trader.order[coin] = 0
            amount[coin] = 0
            trader.blocker[coin]=trader.blocker[coin]-1
        elif 50 > rsindex[coin] >= 40:
            trader.order[coin] = 0
            amount[coin] = 0
            trader.blocker[coin]=trader.blocker[coin]-1
        elif 40 > rsindex[coin] >= 30 and trader.blocker[coin]<=0: 
            trader.order[coin] = 1
            amount[coin] = (1/4)*trader.bank/Hist[-1,coin]
            trader.blocker[coin]=30
        elif 30 > rsindex[coin] >= 20 and trader.blocker[coin]<=0:
            trader.order[coin] = 1
            amount[coin] = (1/2)*trader.bank/Hist[-1,coin]
            trader.blocker[coin]=30
        elif 20 > rsindex[coin] >= 10 and trader.blocker[coin]<=0:
            trader.order[coin] = 1
            amount[coin] = (2/3)*trader.bank/Hist[-1,coin]
            trader.blocker[coin]=30
        elif 10 > rsindex[coin] >= 0 and trader.blocker[coin]<=0:
            trader.order[coin] = 1
            amount[coin] = trader.bank/Hist[-1,coin]
            trader.blocker[coin]=30
    return amount        
    


def JackTrader(Hist, RSI,trader):
    Lookback = int(60)
    sellrisk = 70
    buyrisk = 30
    sellamount = 0.65
    buyamount = 1
    amount=[0,0,0]
    amountcoin = [0,0,0]
    amountcash = [0,0,0]
    for i in range(0,3):
        if RSI[i] > sellrisk and trader.blocker[i]<=0: 
            trader.order[i] = -1
            amount[i] = (sellamount*trader.portfolio[i])*(1-0.0055)
            trader.blocker[i]=50
        elif buyrisk < RSI[i] < sellrisk:
            trader.order[i] = 0
            amount[i] = 0
            trader.blocker[i]=trader.blocker[i]-1
        elif RSI[i] < buyrisk and trader.blocker[i]<=0: 
            trader.order[i] = 1
            amountcoin[i] = (buyamount*trader.bank/Hist[-1,i])*(1-0.0055)
            amountcash[i] = amountcoin[i]*Hist[-1,i]
            amount[i] = np.floor(amountcash[i]/Hist[-1,i]*100)/100
            trader.blocker[i]=50
    return amount


def SmartTrader(Hist, RSI, PredHist, trader):
    Lookback=int(60)
    buffer= 24*60*7
    predi=[0,0,0]
    means=[0,0,0]
    slopes1=[0,0,0]
    slopes2=[0,0,0]
    t=np.array([1,2,3,4])
    tt=np.array(list(range(0,30)))
    mt=2.5
    #Get the predictions
    #Returns predicted average in 5 minutes, will be used to do early trades.
    predi[0] = np.float(PredB(Hist[-Lookback:,0]))
    predi[1] = np.float(PredE(Hist[-Lookback:,1]))
    predi[2] = np.float(PredL(Hist[-Lookback:,2]))
    if np.all(PredHist) and len(PredHist): #Do a prediction correction based 
    #on a running average ratio
        m1=np.sum(PredHist[:6,:],axis=0)/6
        m2=np.sum(Hist[-8:-2,:],axis=0)/6
        predi=predi*m2/m1 #Adjust prediction value depending on previous offsets
    means=[np.mean(Hist[-4:,0]),np.mean(Hist[-4:,1]),np.mean(Hist[-4:,2])]
    #slopes1: t-6:t-2 slope (short term, 2 mins ago)
    slopes1= np.array([np.sum((t-mt)*(Hist[-6:len(Hist)-2,0]-means[0]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-6:len(Hist)-2,1]-means[1]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-6:len(Hist)-2,2]-means[2]))/np.sum((t-mt)*(t-mt))])
    #slopes2: t-4:t slopen (short term, now)
    slopes2= np.array([np.sum((t-mt)*(Hist[-4:,0]-means[0]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-4:,1]-means[1]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-4:,2]-means[2]))/np.sum((t-mt)*(t-mt))])
    #slope : t-30:t slope (long )
    slope=np.polyfit(tt,Hist[-30:,:],1)[0]
    THIRDworth=(np.sum(trader.portfolio*Hist[-1,:])+trader.bank)/3
    maxPortfolio=THIRDworth/Hist[-1,:]
    amount=[0,0,0]
    trader.order=[0,0,0]
    for i in range(0,3):
            #Condition: blocker0/prediction higher than current price/slopes in certain order/RSI below 38 (for risk assessment)/money in bank/no recent buys
        if trader.blocker[i] <=0 and predi[i]>Hist[-1,i] and slope[i]<slopes1[i]<0<slopes2[i] and RSI[i]<38 and trader.bank and trader.tradeworth[i]==0: 
            trader.order[i]=1
            trader.blocker[i]=80
            amount[i]=np.floor(0.8*10*(maxPortfolio[i]-trader.portfolio[i]))/10
            trader.tradeworth[i]=Hist[-1,i]
            #Condition: blocker0/prediction lower than current price/slopes in certain order/ RSI higher 68/coins in portfolio/price now higher than when bought
        if trader.blocker[i] <=0 and predi[i]<Hist[-1,i] and slope[i]>slopes1[i]>0>slopes2[i] and RSI[i]>68 and trader.portfolio[i] and Hist[-1,i]*1.05>trader.tradeworth[i]:
            trader.order[i]=-1
            trader.blocker[i]=80
            amount[i]=np.floor(0.9*10*trader.portfolio[i])/10
            trader.tradeworth[i]=0
            #The following are just securities, if portfolio too valuable, sell, if risk to high, sell, etc.
    if any(trader.portfolio*Hist[-1,:]>THIRDworth*1.5):
        for i in range (0,3):
            if trader.portfolio[i]*Hist[-1,i]>THIRDworth*1.5 and RSI[i]>60:
                trader.order[i]=-1
                amount[i]=maxPortfolio*1.7-trader.portfolio[i]
                trader.blocker[i]=20
                trader.tradeworth[i]=0
    if any(RSI < 17.5):
        for i in range (0,3):
            if RSI[i]<20 and trader.portfolio[i]*Hist[-1,i]<THIRDworth:
                trader.order[i]=1
                amount[i]=maxPortfolio[i]*1.2-trader.portfolio[i]
                trader.blocker[i]=50
                trader.tradeworth[i]=Hist[-1,i]
    if any(RSI > 87.5):
        for i in range (0,3):
            if RSI[i]>87.5:
                trader.order[i]=-1
                trader.blocker[i]=50
                amount[i]=trader.portfolio[i]
                trader.tradeworth[i]=0
    for i in range(0,3):
        if amount[i] == 0 or trader.order[i]==0:
            trader.order[i]=0
            trader.blocker[i]=trader.blocker[i]-1
    return predi, amount


def HillTrade(Hist,trader):
    amount=[0,0,0]
    for j in range (0,3):
        if Hist[-1,j] > Hist[-2,j] > Hist[-4,j]: #If it's going up: SELL
        #Sell the high strategy
            trader.order[j]=-1
            amount[j]=trader.portfolio[j]
        elif Hist[-1,j] < Hist[-2,j] < Hist[-4,j]: #If it's going down: BUY
        #Buy the dip strategy.
            trader.order[j]=1
            amount[j]=np.floor(trader.bank/Hist[-1,j]/3)
        else:
            trader.order[j]=0
            amount[j]=0
        if amount[j]==0:
            trader.order[j]=0
    return amount
            
def LTrader(Hist,rsindex,trader):
    amount=[0,0,0]
    for j in range (0,3):
        if rsindex[j]>75 and trader.blocker[j]<=0: #Do the oposite of Rule trader.
            trader.order[j]=1
            amount[j]=np.floor(trader.bank/Hist[-1,j]/3)
            trader.blocker[j]=50
        elif rsindex[j]<30 and trader.blocker[j] <=0:
            trader.order[j]=-1
            amount[j]=trader.portfolio[j]
            trader.blocker[j]=50
        elif amount[j]==0:
            trader.order[j]=0
            amount[j]=0
            trader.blocker[j]=trader.blocker[j]-1
    return amount

def RandTrader(Hist,trader): 
    amount=[0,0,0]
    trader.order = np.random.randint(3, size=3)-1 #Get a random order array
    #everytime this function is called.
    for j in range(0,3):
        if trader.order[j] == 0:
            amount[j] = 0
        elif trader.order[j] == 1:
            amount[j] = 0.3*trader.bank/Hist[-1,j] #buy 30% of what you could
        elif trader.order[j]==-1 and trader.portfolio[j]: #Sell all you have
            trader.order[j] == -1
            amount[j] = trader.portfolio[j]
    return amount

def InsiderTrader(Hist,rsindex,Inside,trader):
    amount=[0,0,0]
    THIRDworth=(np.sum(trader.portfolio*Hist[-1,:])+trader.bank)/3
    slope=np.polyfit([1,2,3,4,5,6,7,8],Hist[-8:,:],1)[0]
    slope2=np.polyfit([1,2,3],Hist[-3:,:],1)[0]
    maxPortfolio=THIRDworth/Hist[-1,:]
    for j in range(0,3):
        if Inside[j]>1.02*Hist[-1,j] and trader.blocker[j] <=100: #Insider information: price drop/gain of xy% within 1d
            if np.random.randint(10, size=1) == 5: #Only one out of x=10 times he actually gets the info
                trader.order[j]=1
                trader.blocker[j]=1440 #If we know price is going up within a day, wait to trade for a day
                if trader.bank > 1.3*THIRDworth:
                    amount[j]=maxPortfolio*1.25-trader.portfolio[j]
                    trader.tradeworth[j]=Hist[-1,j]*amount
                else:
                    amount[j]=0.7*trader.bank/Hist[-1,j]
            else:
                trader.order[j]=0
        elif Inside[j]<1.02*Hist[-1,j] and trader.blocker[j] <=100 and trader.portfolio[j]:
            if np.random.randint(10, size=1) == 5: #Only one out of x times he actually gets the info
                if rsindex[j] > 80: #Only trade when certain conditions are met
                    trader.order[j]=-1
                    trader.blocker[j]=1440
                    amount[j]=trader.portfolio[j]
                elif rsindex[j] > 65 and slope2[j]<0<slope[j]:
                    trader.order[j]=-1
                    trader.blocker[j]=1440
                    amount[j]=trader.portfolio[j]
                else:
                    trader.blocker[j]=9999
        elif trader.blocker[j]==9999:
            if rsindex[j] > 80: #Only trade when certain conditions are met
                trader.order[j]=-1
                trader.blocker[j]=1440
                amount[j]=trader.portfolio[j]
            elif rsindex[j] > 65 and slope2[j]<0<slope[j]:
                trader.order[j]=-1
                trader.blocker[j]=1440
                amount[j]=trader.portfolio[j]
            else:
                trader.blocker[j]=9999
        elif trader.blocker[j]<=0 and rsindex[j]<25:
            trader.order[j]=1
            amount[j]=maxPortfolio[j]-trader.portfolio[j]
            trader.blocker[j]=100
        elif trader.blocker[j]<=0 and rsindex[j]>70 and slope2[j]<0<slope[j]:
            trader.order[j]=-1
            amount[j]=trader.portfolio[j]
            trader.blocker[j]=100
        elif amount[j]==0 and trader.blocker[j]>-2 and trader.blocker[j] != 9999:
            trader.blocker[j]=trader.blocker[j]-1
    return amount                    
    
def PredTrader(preds, Hist, trader):
    #Based on avanced trader, but much simpler signal generation
    amount=[0,0,0]
    means=[0,0,0]
    slopes1=[0,0,0]
    slopes2=[0,0,0]
    t=np.array([1,2,3,4])
    tt=np.array(list(range(0,30)))
    mt=2.5
    means=[np.mean(Hist[-4:,0]),np.mean(Hist[-4:,1]),np.mean(Hist[-4:,2])]
    slopes1= np.array([np.sum((t-mt)*(Hist[-6:len(Hist)-2,0]-means[0]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-6:len(Hist)-2,1]-means[1]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-6:len(Hist)-2,2]-means[2]))/np.sum((t-mt)*(t-mt))])
    slopes2= np.array([np.sum((t-mt)*(Hist[-4:,0]-means[0]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-4:,1]-means[1]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-4:,2]-means[2]))/np.sum((t-mt)*(t-mt))])
    slope=np.polyfit(tt,Hist[-30:,:],1)[0]
    for j in range(0,3):
        if preds[j]>Hist[-1,j] and trader.blocker[j] <=0 and slope[j]<slopes1[j]<0<slopes2[j]:
            trader.order[j]=1
            amount[j]=trader.bank/Hist[-1,j]/3.1-trader.portfolio[j]
            trader.blocker[j]=50
            trader.tradeworth[j]=Hist[-1,j]
        elif preds[j]<Hist[-1,j] and trader.blocker[j] <=0 and trader.portfolio[j] and Hist[-1,j]>1.05*trader.tradeworth[j] and slope[j]>slopes1[j]>0>slopes2[j]:
            trader.order[j]=-1
            amount[j]=trader.portfolio[j]
            trader.blocker[j]=20
        else:
            trader.order[j]=0
            trader.blocker[j]=trader.blocker[j]-1
    return amount
            
def ShuffleTrader(Hist, RSI,trader):
    #very aggressive, sells coin to be able to afford more of other coins which 
    #should be profitable in the near future. Super Risky.
    Lookback = int(60)
    sellrisk = 70
    buyrisk = 30
    sellamount = 0.65
    buyamount = 1
    amount=[0,0,0]
    amountcoin = [0,0,0]
    amountcash = [0,0,0]
    for i in range(0,3):
        if RSI[i] > sellrisk and trader.blocker[i] <= 0: #and order != 1:
            trader.order[i] = -1
            amount[i] = (sellamount*trader.portfolio[i])*(1-0.0055)
            trader.blocker[i] = 100
        #if RSI > sellrisk and order == 1:
            #order = 0
        elif buyrisk < RSI[i] < sellrisk and trader.blocker[i] <= 0:
            trader.order[i] = 0
            amount[i] = 0
            for m in range(0,3):
                    if RSI[i] > buyrisk > RSI[m] and trader.blocker[m] <= 0:
                        trader.order[i] = -1
                        trader.order[m] = 1
                        trader.blocker[i] = 100
                        trader.blocker[m] = 100
                        amount[i] = (sellamount*trader.portfolio[i])*(1-0.0055)
                        amountcoin[m] = (buyamount*trader.bank/Hist[-1,m])*(1-0.0055)
                        amountcash[m] = amountcoin[m]*Hist[-1,m]
                        amount[m] = np.floor(amountcash[m]/Hist[-1,m]*100)/100
                    else:
                        trader.order[i] = 0
                        amount[i] = 0
                        trader.order[m] = 0
                        amount[m] = 0
        elif RSI[i] < buyrisk and trader.blocker[i] <= 0: #and order != -1:
            trader.order[i] = 1
            amountcoin[i] = (buyamount*trader.bank/Hist[-1,i])*(1-0.0055)
            amountcash[i] = amountcoin[i]*Hist[-1,i]
            amount[i] = np.floor(amountcash[i]/Hist[-1,i]*100)/100
            if amount[i] > trader.bank:
                for m in range(0,3):
                    if RSI[i] > RSI[m]:
                        trader.order[i] = -1
                        trader.order[m] = 1
                        amount[i] = (sellamount*trader.portfolio[i])*(1-0.0055)
                        amountcoin[m] = (buyamount*trader.bank/Hist[-1,m])*(1-0.0055)
                        amountcash[m] = amountcoin[m]*Hist[-1,m]
                        amount[m] = np.floor(amountcash[m]/Hist[-1,m]*100)/100
                    else:
                        trader.order[i] = 0
                        amount[i] = 0
                        trader.order[m] = 0
                        amount[m] = 0
        else:
            trader.order[i] = 0
            amount[i] = 0
            trader.blocker[i] = trader.blocker[i] - 1
    return amount
