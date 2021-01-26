# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 13:42:26 2021

@author: Gamer
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

model16 = keras.models.load_model('PredModels/model16')

#Scaling Factors: Same as Used in Training!
def Pred16(prices):
    mi = 31.8575
    ma = 269.22
    scaled = (prices-mi) / (ma-mi)
    Pr = model16.predict(prices)
    return Pr



#Good models: 14, (15?), 16, 17

t1=24*60*7

df = pd.read_csv ("Ether_Min_Jan20.csv")
raw = df.iloc[0:t1,np.array([5,6])]
raw2 = df.iloc[0:2*t1,np.array([5,6])]

  


sc_cl = MinMaxScaler(feature_range = (0, 1))
sc_classic = sc_cl.fit_transform(raw2)


Lookback=70 #Amount of Inputs
Window = 10 #Amount of Datapoints to Calc run Mean (EVEN)
Outlook = 1 #Amount of Outputs

scaled=raw
scaled2=raw2

#Make the range larger so all values are around 0.3-0.7
mi = min(raw2.iloc[0:int(t1/2),0])/4
ma = max(raw2.iloc[0:int(t1/2),0])*2