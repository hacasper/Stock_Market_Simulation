# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:49:51 2021

@author: Lionel
"""

#Libraries 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Import CSV data
AAPL = pd.read_csv ("AAPL.csv")
#Needed to clean data as there are NAN rows
AAPL=AAPL.dropna()
AAPL=pd.DataFrame(AAPL)
row_count = AAPL.shape[0]
days_ma_1 = 10
days_ma_2 = 40

#Depending on moving Average chosen above set t0
t0=max(days_ma_1,days_ma_2)
horizon=row_count-t0

#Generating Empty Array to Save the moving averages for later eval

Means = np.empty([horizon,2])
Slopes = np.empty([horizon,2])
#Start simulating time
for t in range(t0,row_count):
    #Gives me the indices for first moving average
    t1 = list(range(t-days_ma_1,t))
    Set1=AAPL.iloc[t1,:]
    Sum1=Set1.sum(axis=0)
    #Gives me the indeces for second moving average
    t2 = list(range(t-days_ma_2,t))
    Set2=AAPL.iloc[t2,:]
    Sum2=Set2.sum(axis=0)
    #Means at t-t0 will give you most recent moving average
    Means[t-t0,0]=Sum1[6]/days_ma_1
    Means[t-t0,1]=Sum2[6]/days_ma_2
    
    #Trendline Calculations
    Set1=Set1.iloc[:,6]
    Set2=Set2.iloc[:,6]
    slope1 = np.polyfit(Set1.index, Set1, 1)[0]
    slope2 = np.polyfit(Set2.index, Set2, 1)[0]
    Slopes[t-t0,0]=slope1
    Slopes[t-t0,1]=slope2
    t=t+1
   
    
Day=list(range(0,horizon))
plt.plot(Day, Slopes[:,0])
plt.plot(Day, Slopes[:,1])
plt.legend(['10-day MAV','40-day MAV'])
    

    
