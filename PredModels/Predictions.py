# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:52:27 2021
@author: Lionel
"""
# Source: https://www.kdnuggets.com/2018/11/keras-long-short-term-memory-lstm-model-predict-stock-prices.html

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler



def MiMaScaler(data, mi, ma, i):
    sca = (data.iloc[i:,:] - mi)/(ma - mi)
    return sca.iloc[:,:]


#Good models: 14, (15?), 16, 17

#model 18: 60, 50, 10(5)
#model 19: 75, 60, 10(5)

#Final Models
#Model 20: ETHER, 75 Lookback, 60 nodes, Outlook = Av in 5min, 


t1=24*60*7

df = pd.read_csv ('../Data/Ether_Min_Jan20.csv')
raw = df.iloc[0:t1,np.array([5,6])]
raw2 = df.iloc[0:2*t1,np.array([5,6])]
size=raw2.shape[0]
  

Lookback=75 #Amount of Inputs
Window = 10 #Amount of Datapoints to Calc run Mean (EVEN)
Outlook = 1 #Amount of Outputs

#Without Differences: Use scaled
scaled=raw2

#With Differences: Use dif
dif=np.zeros(size-1)


#Differences Trial:
for i in range(0,size-1):
    dif[i]=raw2.iloc[i+1,1]-raw2.iloc[i,1]

#Make the range larger so all values are around 0.3-0.7 for scaled approach
mi = min(raw2.iloc[0:int(t1/2),0])/4
ma = max(raw2.iloc[0:int(t1/2),0])*2

#Double the differences for better compatibility with extreme values
mi2 = min(dif)*2.5
ma2 = max(dif)*2.5

scaled = (scaled.iloc[:,:]-mi) / (ma - mi)

difscaled = (dif-mi2) / (ma2-mi2)

sfac = np.full([2*t1,2],[mi,ma])
# for i in range (int(t1/2), 2*t1):
#     if raw2.iloc[i, 0]>ma:
#         ma=raw2.iloc[i, 0]
#         sfac[i:,1]=ma
#     if raw2.iloc[i, 0]<mi:
#         mi=raw2.iloc[i, 0]
#         sfac[i:,0]=mi
#     scaled2.iloc[i:,:]=MiMaScaler(raw2,mi, ma,i)


X_train = []
X_test = []
y_train = []
for j in range (Lookback, t1-Window-Window):
    Means = sum(scaled2.iloc[j+int(Window/2):j+int(Window/2)+Window,0])/Window
    X_train.append(scaled2.iloc[j-Lookback:j, 0])
    X_test.append(scaled2.iloc[t1-Lookback+j:t1+j,0])
    y_train.append(Means)
    
    



X_train, y_train  = np.array(X_train), np.array(y_train)
X_test = np.array(X_test)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


regressor = Sequential()

regressor.add(LSTM(units = 60, return_sequences = True, input_shape = (X_train.shape[1], 1)))

regressor.add(LSTM(units = 60, return_sequences = True))
regressor.add(Dropout(0.1))

regressor.add(LSTM(units = 60, return_sequences = True))
regressor.add(Dropout(0.1))

regressor.add(LSTM(units = 60))

regressor.add(Dense(units = Outlook)) #Amount of Outputs

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 75, batch_size = 50)

pred = pd.DataFrame(regressor.predict(X_test))

t=np.array(list(range(0,2*t1)))


regressor.save('model20')


plt.plot(t[Lookback:],scaled2.iloc[Lookback:,0])

plt.plot(t[t1+3:2*t1-Lookback+3-Window-Window],pred.iloc[:,0])
plt.show()
#t1=t1+50
a=0
mrks=list(range(a,a+300,10))
x=list(range(t1+a,t1+a+300,10))
plt.plot(t[t1+a:t1+300+a],scaled2.iloc[t1+a:t1+300+a,0])
plt.plot(t[x],pred.iloc[mrks,0],marker="o") 
plt.show()

x=list(range(t1+a,t1+a+500,50))
mrks=list(range(a,a+500,50))
plt.plot(t[t1+a:t1+a+500],scaled2.iloc[t1+a:t1+a+500,0])
plt.plot(t[x],pred.iloc[mrks,0],marker="o")
# plt.plot(t[t1+10:t1+12],pred.iloc[10,:]) 
# plt.plot(t[t1+20:t1+22],pred.iloc[20,:]) 
# plt.plot(t[t1+30:t1+32],pred.iloc[30,:]) 
# plt.plot(t[t1+40:t1+42],pred.iloc[40,:]) 
plt.show()