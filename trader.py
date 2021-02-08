# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 13:42:26 2021

@author: Lionel
"""
import pandas as pd
import datetime as dt
import math
import csv  
import numpy as np


def RSIblind(Hist,RSP,t,gain,loss,RSI):
    Lookback=75
    if RSI == 0: #There is a mistake somewhere here, the else statement is correct
        val=Hist[Lookback-RSP:Lookback+1,3]
        var1=np.diff(val)
        dim=var1.size
        
        gain = 0.000001
        loss = 0.000001
        for i in range(0,dim-1):
            if var1[i]>0:
                gain = gain + var1[i]
            else:
                loss = loss - var1[i]
        rs = gain/loss
        gain=gain/14
        loss=loss/14
        rsi = 100-(100/(1+rs))
        return gain, loss, rsi 
    else:
        val=Hist[Lookback-RSP:Lookback+1,3]
        var1=np.diff(val)
        if var1[RSP-2] > 0:
            cg = var1[RSP-2]
            cl = 0
        else:
            cl = -var1[RSP-2]
            cg = 0
        gain = (gain*(RSP-2)+cg)/14
        loss = (loss*(RSP-2)+cl)/14  
        rsi = 100-(100/(1+(gain)/(loss)))       
        return gain, loss, rsi
        
    
def StupidTrader(Hist, RSP,t,gain,loss,RSI,trader,coin):
    Lookback=75
    gain, loss, rsindex = RSIblind(Hist,RSP,t,gain,loss,RSI)
    if rsindex > 70: #and order != 1:
        trader.order[coin] = -1
        amount = trader.portfolio[coin]
    #if RSI > 70 and order == 1:
        #order = 0
    elif 30 < rsindex < 70:
        trader.order[coin] = 0
        amount = 0
    elif rsindex < 30: #and order != -1:
        trader.order[coin] = 1
        amount = np.floor(trader.bank[coin]/Hist[Lookback,3])
    #if RSI < 30 and order == -1:
        #order = 0
    return loss, gain, rsindex, amount

def SmartTrader(Hist, RSP, t, gain, loss, RSI, trader, coin):
    Lookback=75
    
    
    
    return Preds, amount
    
    
    