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
from tensorflow.keras.models import load_model
#Final Models
#Model 20: ETHER, 60 Lookback, 50 nodes, Outlook = Av in 4min, without trend correction
#Model 24(1): Bitcoin, samesamem, TRIAL, see model 23 and 24 for comparison &31
#Model 22: Litecoin, samesamem, see also 25&maybe 26&27&28&29

t1=int(24*60*7)
Lookback=60 #Amount of Inputs
Window = 4 #Amount of Datapoints to Calc run Mean 
Outlook = 1 #Amount of Outputs

df = pd.read_csv ('../Data/Lite_Min_Jan20.csv') #Read the Data you want to model for
raw = df.iloc[0:2*t1,np.array([8,6])] #selects 2*buffer for training and test training
size = raw.shape[0] #size of train + test data
t = np.array(list(range(0,size))) #ind array for train + test data

ADJ=raw.iloc[:,0] #I actually only need the closing prices

#Double the differences for better compatibility with extreme values (only access training data)
mi = min(ADJ.iloc[0:int(24*60*7)])/4
ma = max(ADJ.iloc[0:int(24*60*7)])*2

#The effect of rising stock prices over increased periods of time will be
#taken into account in the trader function itsaelf for models 40+ (running average correction)


scaled = (ADJ.iloc[:]-mi) / (ma - mi)

X_train = []
X_test = []
y_train = []
for j in range (Lookback, t1-Window):
    Means = sum(scaled.iloc[j+2:j+Window+2])/Window
    X_train.append(scaled.iloc[j-Lookback:j])
    X_test.append(scaled.iloc[t1-Lookback+j:t1+j])
    y_train.append(Means)
    
    
# X_train=X_train2
# X_test=X_test2
# y_train=y_train2


X_train, y_train  = np.array(X_train), np.array(y_train)
X_test = np.array(X_test)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.1))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.1))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.1))

regressor.add(LSTM(units = 50))

regressor.add(Dense(units = Outlook)) #Amount of Outputs

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 50, batch_size = 50)

pred = pd.DataFrame(regressor.predict(X_test))

regressor.save('model52')

     
plt.plot(t[0:],scaled.iloc[0:])
plt.plot(t[int(t1):2*t1-Lookback-Window],pred.iloc[:,0])
plt.show()
#t1=t1+50
a=5000
mrks=list(range(a,a+300,2))
x=list(range(t1+a,t1+a+300,2))
plt.plot(t[t1+a:t1+300+a],scaled.iloc[t1+a:t1+300+a])
plt.plot(t[x],pred.iloc[mrks,0],marker="o") 
plt.show()

x=list(range(t1+a,t1+a+500,2))
mrks=list(range(a,a+500,2))
plt.plot(t[t1+a:t1+a+500],scaled.iloc[t1+a:t1+a+500])
plt.plot(t[x],pred.iloc[mrks,0],marker="o")
# plt.plot(t[t1+10:t1+12],pred.iloc[10,:]) 
# plt.plot(t[t1+20:t1+22],pred.iloc[20,:]) 
# plt.plot(t[t1+30:t1+32],pred.iloc[30,:]) 
# plt.plot(t[t1+40:t1+42],pred.iloc[40,:]) 
plt.show()


# plt.plot(t[t1:2*t1-Window-Window-Lookback],y_train)
# plt.plot(t[t1:2*t1-Window-Window-Lookback],pred.iloc[:,0])
# plt.legend('1','2')
# plt.show()

# mB = load_model("PredModels/model31")
# mE = load_model("PredModels/model20")
# mL = load_model("PredModels/model20")
