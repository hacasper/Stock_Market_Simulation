# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:21:53 2021

@author: saber
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
    
    
#IDK how to call n so that it carries to market fucntion
    
def TieredTrader(Hist, RSP,t,gain,loss,RSI,trader,coin):
    Lookback=75
    gain, loss, rsindex = RSIblind(Hist,RSP,t,gain,loss,RSI)
    if 100 > rsindex >= 90: #and order != 1:
        trader.order[coin] = -1
        amount = trader.portfolio[coin]
    #if RSI > 70 and order == 1:
        #order = 0
    elif 90 > rsindex >= 80: #and order != 1:
        trader.order[coin] = -1
        amount = (2/3)*trader.portfolio[coin]
    elif 80 > rsindex >= 70: #and order != 1:
        trader.order[coin] = -1
        amount = (1/2)*trader.portfolio[coin]
    elif 70 > rsindex >= 60: #and order != 1:
        trader.order[coin] = -1
        amount = (1/4)*trader.portfolio[coin]
    elif 60 > rsindex >= 50: #and order != 1:
        trader.order[coin] = 0
        amount = 0
    elif 50 > rsindex >= 40: #and order != 1:
        trader.order[coin] = 0
        amount = 0
    elif 40 > rsindex >= 30: #and order != 1:
        trader.order[coin] = 1
        amount = (1/4)*trader.bank[coin]
    elif 30 > rsindex >= 20: #and order != 1:
        trader.order[coin] = 1
        amount = (1/2)*trader.bank[coin]
    elif 20 > rsindex >= 10: #and order != 1:
        trader.order[coin] = 1
        amount = (2/3)*trader.bank[coin]
    elif 10 > rsindex >= 0: #and order != 1:
        trader.order[coin] = 1
        amount = trader.bank[coin]
    #if RSI < 30 and order == -1:
        #order = 0
    return loss, gain, rsindex, amount