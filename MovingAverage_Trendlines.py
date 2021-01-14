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
MeanCorr = np.empty([horizon,2])
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
    
    #New Means based on Trendline
    x1=np.array(list(range(1,int(days_ma_1/2)+1)))
    x2=np.array(list(range(1,int(days_ma_2/2)+1)))
    y1=Set1.iloc[days_ma_1-1]+Slopes[t-t0,0]*x1
    y2=Set2.iloc[days_ma_2-1]+Slopes[t-t0,1]*x2
    
    cSet1=np.array(Set1.iloc[x1.size:days_ma_1])
    cSet2=np.array(Set2.iloc[x2.size:days_ma_2])
    yPred1=Set1.iloc[Set1.size-1]+slope1*x1
    yPred2=Set2.iloc[Set2.size-1]+slope2*x2
    MeanCorr[t-t0,0]=(sum(yPred1)+sum(cSet1))/days_ma_1
    MeanCorr[t-t0,1]=(sum(yPred2)+sum(cSet2))/days_ma_2
    
    t=t+1
   
    
Day=list(range(0,horizon))
PredDay=np.array(list(range(t0,row_count)))
plt.plot(Day, Means[:,0])
plt.plot(Day, Means[:,1])
plt.plot(PredDay-t0, AAPL.iloc[PredDay,6])
plt.legend(['10-day MAV','40-day MAV','Daily Closing'])
plt.show()

#New plot with trendline corrected average daily means (all linear fit)
plt.plot(Day,MeanCorr[:,0])
plt.plot(Day,MeanCorr[:,1])
plt.plot(PredDay-t0, AAPL.iloc[PredDay,6])
plt.legend(['10-day MAV','40-day MAV','Daily Closing'])
plt.show()

    
