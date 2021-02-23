# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 13:42:26 2021

@author: Lionel
"""
from preds import PredB, PredE, PredL
import numpy as np


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
    gain, loss, rsindex = RSIblind(Hist,RSP,gain,loss,RSI)
    amount=[0,0,0]
    for j in range (0,3):
        if rsindex[j] > 70: #and order != 1:
            trader.order[j] = -1
            amount[j] = trader.portfolio[j]
        #if RSI > 70 and order == 1:
            #order = 0
        elif 35 < rsindex[j] < 70:
            trader.order[j] = 0
            amount[j] = 0
        elif rsindex[j] < 30: #and order != -1:
            trader.order[j] = 1
            amount[j] = np.floor(trader.bank/Hist[-1,j]/30)
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
            amount[i] = buyamount*np.floor(trader.bank/Hist[-1,i])
        #if RSI < buyrisk and order == -1:
            #order = 0
    return amount

def SmartTrader(Hist, RSI, trader):
    Lookback=int(60)
    buffer= 24*60*7
    predi=[0,0,0]
    #Get the predictions
    #Returns predicted average in 5 minutes, will be used to do early trades.
    predi[0] = PredB(Hist[-Lookback:,0])
    predi[1] = PredE(Hist[-Lookback:,1])
    predi[2] = PredL(Hist[-Lookback:,2])
    amount=[0,0,0]
    THIRDworth=(np.sum(trader.portfolio*Hist[buffer+np.shape(trader.transactions)[0]-1,:])+trader.bank)/3
    for j in range (0,3):
        if trader.portfolio[j]*Hist[-1,j] > THIRDworth:
            trader.order[j] = -1
            amount[j]=np.ceil((trader.portfolio[j]-THIRDworth)/Hist[-1,j])
            
        
        
        
        if RSI[j] > 70 and predi[j] < Hist[-1,j]: #selling only if preds is lower than price right now
            trader.order[j] = -1
            amount[j] = trader.portfolio[j]
        elif RSI[j] > 70:
            trader.order[j] = -1
            amount[j] = np.ceil(trader.portfolio[j]*0.8)
        elif 30 < RSI[j] < 70:
            trader.order[j] = 0
            amount[j] = 0
        elif RSI[j] < 40 and predi[j] > np.mean(Hist[-6:,j]): #
            trader.order[j] = 1
            amount[j] = np.floor(trader.bank/Hist[-1,j]/10)
        elif RSI[j] < 30:
            trader.order[j] = 1
            amount[j] = np.floor(trader.bank/Hist[-1,j]/20)
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
            amount[j]=trader.portfolio[j]
        elif Hist[-1,j] < Hist[-2,j] < Hist[-3,j]:
            trader.order[j]=-1
            amount[j]=np.floor(trader.bank/Hist[-1,j]/3)
        else:
            trader.order[j]=0
            amount[j]=0
    return amount