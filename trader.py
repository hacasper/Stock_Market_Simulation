# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 13:42:26 2021

@author: Lionel
"""
from preds import PredB, PredE, PredL
import numpy as np
import math
import random

def RSIblind(Hist,RSP,gain,loss,RSI):
    Lookback=int(60)
    rs=[0,0,0]
    rsind=[0,0,0]
    if RSI[0] == RSI[1] == RSI[2] == 0: #Initialize RSI
        val=Hist[-RSP:,:]
        var1=np.diff(val,axis=0)
        dim=var1.shape[0]
        for j in range(0,3): #Loop over 3 Coins
            gain[j] = 0.000001
            loss[j] = 0.000001
            for i in range(0,dim-1): #Loop over RSP
                if var1[i,j]>0:
                    gain[j] = gain[j] + var1[i,j] #add gains
                else:
                    loss[j] = loss[j] - var1[i,j] #add losses
            rs[j] = gain[j]/loss[j] #calculate 3 RS
            gain[j]=gain[j]/14
            loss[j]=loss[j]/14
            rsind[j] = 100-(100/(1+rs[j]))
        return gain, loss, rsind #Return 3*(gain, loss, rsind) for the 3 coins
    else:
        val=Hist[-RSP:,:]
        var1=np.diff(val,axis=0)
        for j in range(0,3):
            if var1[-1,j] > 0:
                cg = var1[-1,j]
                cl = 0
            else:
                cl = -var1[-1,j]
                cg = 0
            gain[j] = (gain[j]*(RSP-2)+cg)/14
            loss[j] = (loss[j]*(RSP-2)+cl)/14  
            rsind[j] = 100-(100/(1+(gain[j])/(loss[j])))       
        return gain, loss, rsind
        
    
def StupidTrader(Hist,RSP,gain,loss,RSI,trader):
    Lookback=int(60)
    fac=0.2
    THIRDworth=(np.sum(trader.portfolio*Hist[-1,:])+trader.bank)/3
    maxPortfolio=THIRDworth/Hist[-1,:]
    gain, loss, rsindex = RSIblind(Hist,RSP,gain,loss,RSI)
    amount=[0,0,0]
    for j in range (0,3):
        if rsindex[j] > 70: #and order != 1:
            trader.order[j] = -1
            amount[j] = np.floor(fac*trader.portfolio[j]*10)/10
        #if RSI > 70 and order == 1:
            #order = 0
        elif 35 < rsindex[j] < 70:
            trader.order[j] = 0
            amount[j] = 0
        elif rsindex[j] < 30: #and order != -1:
            trader.order[j] = 1
            amount[j] = np.floor(fac*(maxPortfolio[j]-trader.portfolio[j])*10)/10
    return loss,gain,rsindex,amount
    
def TieredTrader(Hist,rsindex,trader):
    #Lookback=75
    amount=[0,0,0]
    for coin in range (0,3):
        if 100 > rsindex[coin] >= 90: #and order != 1:
            trader.order[coin] = -1
            amount[coin] = trader.portfolio[coin]
        #if RSI > 70 and order == 1:
            #order = 0
        elif 90 > rsindex[coin] >= 80: #and order != -1:
            trader.order[coin] = -1
            amount[coin] = (2/3)*trader.portfolio[coin]
        elif 80 > rsindex[coin] >= 70: #and order != -1:
            trader.order[coin] = -1
            amount[coin] = (1/2)*trader.portfolio[coin]
        elif 70 > rsindex[coin] >= 60: #and order != -1:
            trader.order[coin] = -1
            amount[coin] = (1/4)*trader.portfolio[coin]
        elif 60 > rsindex[coin] >= 50: #and order != 1:
            trader.order[coin] = 0
            amount[coin] = 0
        elif 50 > rsindex[coin] >= 40: #and order != 1:
            trader.order[coin] = 0
            amount[coin] = 0
        elif 40 > rsindex[coin] >= 30: #and order != 1:
            trader.order[coin] = 1
            amount[coin] = (1/4)*trader.bank/Hist[-1,coin]
        elif 30 > rsindex[coin] >= 20: #and order != 1:
            trader.order[coin] = 1
            amount[coin] = (1/2)*trader.bank/Hist[-1,coin]
        elif 20 > rsindex[coin] >= 10: #and order != 1:
            trader.order[coin] = 1
            amount[coin] = (2/3)*trader.bank/Hist[-1,coin]
        elif 10 > rsindex[coin] >= 0: #and order != 1:
            trader.order[coin] = 1
            amount[coin] = trader.bank/Hist[-1,coin]
        #if RSI < 30 and order == -1:
            #order = 0
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
        if RSI[i] > sellrisk: #and order != 1:
            trader.order[i] = -1
            amount[i] = sellamount*trader.portfolio[i]
        #if RSI > sellrisk and order == 1:
            #order = 0
        elif buyrisk < RSI[i] < sellrisk:
            trader.order[i] = 0
            amount[i] = 0
        elif RSI[i] < buyrisk: #and order != -1:
            trader.order[i] = 1
            amountcoin[i] = buyamount*trader.bank/Hist[-1,i]
            amountcash[i] = amountcoin[i]*Hist[-1,i]
            amount[i] = np.floor(amountcash[i]/Hist[-1,i]*100)/100
        #if RSI < buyrisk and order == -1:
            #order = 0
    return amount


def SmartTrader(Hist, RSI, PredHist, trader):
    Lookback=int(60)
    buffer= 24*60*7
    predi=[0,0,0]
    means=[0,0,0]
    slopes1=[0,0,0]
    slopes2=[0,0,0]
    t=np.array([1,2,3,4])
    mt=2.5
    #Get the predictions
    #Returns predicted average in 5 minutes, will be used to do early trades.
    predi[0] = np.float(PredB(Hist[-Lookback:,0]))
    predi[1] = np.float(PredE(Hist[-Lookback:,1]))
    predi[2] = np.float(PredL(Hist[-Lookback:,2]))
    if np.all(PredHist) and len(PredHist):
        m1=np.sum(PredHist[:6,:],axis=0)/6
        m2=np.sum(Hist[-6:,:],axis=0)/6
        predi=predi*m2/m1
    means=[np.mean(Hist[-4:,0]),np.mean(Hist[-4:,1]),np.mean(Hist[-4:,2])]
    slopes1= np.array([np.sum((t-mt)*(Hist[-6:len(Hist)-2,0]-means[0]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-6:len(Hist)-2,1]-means[1]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-6:len(Hist)-2,2]-means[2]))/np.sum((t-mt)*(t-mt))])
    slopes2= np.array([np.sum((t-mt)*(Hist[-4:,0]-means[0]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-4:,1]-means[1]))/np.sum((t-mt)*(t-mt)),np.sum((t-mt)*(Hist[-4:,2]-means[2]))/np.sum((t-mt)*(t-mt))])
    THIRDworth=(np.sum(trader.portfolio*Hist[-1,:])+trader.bank)/3
    maxPortfolio=THIRDworth/Hist[-1,:]
    dif=slopes2-slopes1
    amount=[0,0,0]
    trader.order=[0,0,0]
    for i in range(0,3):
        '''
        If sloppes1[i]<0 and slopes2[i]>0 and predi[i]>Hist[-1,i]:
            buy
        elif opposite
            sell
        '''
        if predi[i]>Hist[-1,i] and dif[i]>0 and RSI[i]<40 and trader.bank:
            trader.order[i]=1
            amount[i]=np.floor(0.4*10*(maxPortfolio[i]-trader.portfolio[i]))/10
        elif predi[i]>Hist[-1,i] and dif[i]>0 and RSI[i]<50 and trader.bank:
            trader.order[i]=1
            amount[i]=np.floor(0.2*10*(maxPortfolio[i]-trader.portfolio[i]))/10
        elif predi[i]>Hist[-1,i] and RSI[i]<50 and trader.bank:
            trader.order[i]=1
            amount[i]=np.floor(0.2*10*(maxPortfolio[i]-trader.portfolio[i]))/10
        elif dif[i]>0 and RSI[i]<50 and trader.bank:
            trader.order[i]=1
            amount[i]=np.floor(0.2*10*(maxPortfolio[i]-trader.portfolio[i]))/10
        if predi[i]<Hist[-1,i] and dif[i]<0 and RSI[i]>70 and trader.portfolio[i]:
            trader.order[i]=-1
            amount[i]=np.floor(0.4*10*trader.portfolio[i])/10
        elif predi[i]<Hist[-1,i] and dif[i]<0 and trader.portfolio[i]:
            trader.order[i]=-1
            amount[i]=np.floor(0.2*10*trader.portfolio[i])/10
        elif predi[i]<Hist[-1,i] and RSI[i]>70 and trader.portfolio[i]:
            trader.order[i]=-1
            amount[i]=np.floor(0.2*10*trader.portfolio[i])/10
        elif dif[i]<0 and RSI[i]>70 and trader.portfolio[i]:
            trader.order[i]=-1
            amount[i]=np.floor(0.2*10*trader.portfolio[i])/10
        # if predi[i]>Hist[-1,i]:
        #     trader.order[i]=1
        #     amount[i]=0.2*(maxPortfolio[i]-trader.portfolio[i])
        # if predi[i]<Hist[-1,i]:
        #     trader.order[i]=-1
        #     amount[i]=0.2*trader.portfolio[i]
            
            
    if any(trader.portfolio*Hist[-1,:]>THIRDworth*1.2):
        for i in range (0,3):
            if trader.portfolio[i]*Hist[-1,i]>THIRDworth*1.2 and RSI[i]>60:
                trader.order[i]=-1
                amount[i]=maxPortfolio*1.2-trader.portfolio[i]
    if any(RSI < 17.5):
        for i in range (0,3):
            if RSI[i]<20 and trader.portfolio[i]*Hist[-1,i]<THIRDworth:
                trader.order[i]=1
                amount[i]=maxPortfolio[i]*0.2-trader.portfolio[i]
    if any(RSI > 87.5):
        for i in range (0,3):
            if RSI[i]>87.5:
                trader.order[i]=-1
                amount[i]=trader.portfolio[i]
    return predi, amount


def HillTrade(Hist,trader):
    amount=[0,0,0]
    for j in range (0,3):
        if Hist[-1,j] > Hist[-2,j] > Hist[-3,j]:
            trader.order[j]=-1
            amount[j]=trader.portfolio[j]
        elif Hist[-1,j] < Hist[-2,j] < Hist[-3,j]:
            trader.order[j]=1
            amount[j]=np.floor(trader.bank/Hist[-1,j]/3)
        else:
            trader.order[j]=0
            amount[j]=0
    return amount
            
def LTrader(Hist,trader):
    amount=[0,0,0]
    for j in range (0,3):
        if Hist[-1,j] > Hist[-2,j] > Hist[-3,j]:
            trader.order[j]=1
            amount[j]=np.floor(trader.bank/Hist[-1,j]/3)
        elif Hist[-1,j] < Hist[-2,j] < Hist[-3,j]:
            trader.order[j]=-1
            amount[j]=trader.portfolio[j]
        else:
            trader.order[j]=0
            amount[j]=0
    return amount

def RandTrader(Hist,trader):
    amount=[0,0,0]
    trader.order = np.random.randint(3, size=3)-1
    for j in range(0,3):
        if trader.order[j] == 0:
            amount[j] = 0
        elif trader.order[j] == 1:
            amount[j] = 0.9*trader.bank/Hist[-1,j]
        else: 
            trader.order[j] == -1
            amount[j] = trader.portfolio[j]
    return amount            
    

        
        