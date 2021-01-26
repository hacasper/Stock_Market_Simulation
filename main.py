import pandas as pd
import datetime as dt
import math
import csv  
import numpy as np
import matplotlib.pyplot as plt


from Classes import trader 
from Classes import market


dfBTC = pd.read_csv ("Bitcoin_Min_Jan20.csv")
df = pd.read_csv ("Ether_Min_Jan20.csv")
dim=df.shape[0]

#pd.concat([dfBTC,dfETH]).drop_duplicates(subset = ['col2'], keep=False)

buffer=24*60*7 #1 Week data to use for models

horizon=dim-buffer #amount of timestamps in the for loop


#########################
base = dt.date(2020, 1, 1)
arr = list([base + dt.timedelta(weeks=i) for i in range(5)])
tik = list([-buffer, 0, buffer, 2*buffer, 3*buffer])

Mins=np.array(list(range(0,horizon)))
ng=np.array(list(range(-buffer,0)))
plt.title('Etherum Stockdata January 2020')
plt.plot(ng,df.iloc[0:buffer,8])
plt.plot(Mins,df.iloc[buffer:dim,8])
plt.legend(['Data used for Models and Trends','Data used for Simulation'])
plt.vlines(0,min(df.iloc[0:dim,8]),max(df.iloc[0:dim,8]),colors='k',linestyles='dashed')
plt.xticks(tik,arr)
plt.show()
#########################

#Once we have models that work we either pull recent data and test  on that
#or we can just use only partial amounts of the datasets to calibrate and then test


Closing = np.empty([horizon,1])
Hist = np.empty([horizon,4])
Hist[0:buffer-1,:] = np.array(df.iloc[0:buffer-1,5:9])
m=market('ETH',df.iloc[buffer-1,1],df.iloc[buffer-1,5])


def main():
    for t in range (buffer,dim):
        #indices: 10=trades, 9=volume, 8=close, 7=low, 6=high, 5=open, 1 time open

        #get market price at time t

        #prediction
        #output will be average price in 5 minutes

        #get RSI from RSICalculator.py

        #trader: using RSI and market price make trading decision

        #update trader's portfolio/bank value based on trading decision

        #Current Market with opening timestamp: 
        m=market('ETH',df.iloc[t,1],df.iloc[t,5])
        Closing[t-buffer]=m.price
        
        if t % 1000 == 0:
            print("market price for " + m.ticker + " on " + m.date + " is " + str(m.price))
            
        Hist[t,:]=np.array(df.iloc[t,5:9])

if __name__ == "__main__":
    main()