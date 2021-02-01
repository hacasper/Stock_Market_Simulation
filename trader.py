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
    if RSI == 0:
        val=Hist[t-RSP:t,0]
        var1=np.diff(val)
        dim=var1.size
        
        gain = 0
        loss = 0
        for i in range(0,dim-1):
            if var1[i]>0:
                gain = gain + var1.iloc[i]
            else:
                loss = loss - var1.iloc[i]
        rs = gain/loss
        rsi = 100-(100/(1+rs))
        return gain, loss, rsi 
    else:
        if var1[RSP-1] > 0:
            cg = var1[RSP-1]
            cl = 0
        else:
            cl = -var1[RSP-1]
            cg = 0
        gain = gain*(RSP-1)+cg
        loss = loss*(RSP-1)+cl
        rsi = 100-(100/(1+(gain*(RSP-1)+cg)/(loss*(RSP-1)+cl)))       
        return gain, loss, rsi
        
    
def StupidTrader(Hist, RSP,t,gain,loss,RSI,order):
    gain, loss, RSI = RSIblind(Hist,RSP,t,gain,loss,RSI)
    if RSI > 70 and order != 1:
        order = 1
    if RSI > 70 and order == 1:
        order = 0
    if 30 < RSI < 70:
        order = 0
    if RSI < 30 and order != -1:
        order = -1
    if if RSI < 30 and order == -1:
        order = 0
    return order