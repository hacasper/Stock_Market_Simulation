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
        val=Hist[t-RSP:t,3]
        var1=np.diff(val)
        dim=var1.size
        
        gain = 0
        loss = 0
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
        val=Hist[t-RSP:t,3]
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
        
    
def StupidTrader(Hist, RSP,t,gain,loss,RSI,order):
    gain, loss, rsindex = RSIblind(Hist,RSP,t,gain,loss,RSI)
    if rsindex > 70: #and order != 1:
        order = 1
    #if RSI > 70 and order == 1:
        #order = 0
    if 30 < rsindex < 70:
        order = 0
    if rsindex < 30: #and order != -1:
        order = -1
    #if RSI < 30 and order == -1:
        #order = 0
    return order, loss, gain, rsindex