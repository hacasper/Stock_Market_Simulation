# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:52:27 2021

@author: Lionel
"""
# Source: https://www.kdnuggets.com/2018/11/keras-long-short-term-memory-lstm-model-predict-stock-prices.html

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv ("Ether_Min_Jan20.csv")
raw = df.iloc[:,np.array([5,6])]

scaler = MinMaxScaler(feature_range = (0, 1))
scaled = scaler.fit_transform(raw)

X_train = []
X_test = []
y_train = []

Lookback=60 #(1/12 of overall buffer)

t1=9180


for i in range(Lookback, t1):
    X_train.append(scaled[i-Lookback:i, 0])
    X_test.append(scaled[t1-Lookback+i:t1+i,0])
    y_train.append(scaled[i:i+10, 0])
    
    



X_train, y_train  = np.array(X_train), np.array(y_train)
X_test = np.array(X_test)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 10)) #Amount of Outputs

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 100, batch_size = 50)

pred = pd.DataFrame(regressor.predict(X_test))

t=list(range(0,2*t1))


regressor.save('model3')


plt.plot(t,scaled[0:2*t1,0])
plt.plot(t[t1:2*t1],pred.iloc[:,0]) 