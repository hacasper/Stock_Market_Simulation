# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 13:42:26 2021

@author: Lionel
"""

# Source: https://www.kdnuggets.com/2018/11/keras-long-short-term-memory-lstm-model-predict-stock-prices.html

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
mo40 = load_model("PredModels/model40")
mo41 = load_model("PredModels/model41")
mo42 = load_model("PredModels/model42")  


 # mod6 = load_model('PredModels/model16/')


# Scaling Factors: Same as Used in Training!
# def Pred16(prices):
#     Lookback = 60
#     mi = 31.8575
#     ma = 269.22
#     scaled = (prices[t-1-Lookback:t-1]-mi) / (ma-mi)
#     X_test = np.array(scaled)
#     X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
#     Prsc = mo16.predict(X_test)
#     Pr = Prsc*(ma-mi)+mi
#     return Pr

def PredB(prices):
    mi = 1714.555
    ma = 16583.8
    scaled = (prices-mi) / (ma-mi)
    X_test = np.array(scaled)
    X_test = np.reshape(X_test, (1, X_test.shape[0], 1))
    Prsc = mo40.predict(X_test)
    Pr = Prsc*(ma-mi)+mi
    return Pr 

def PredE(prices):
    mi = 31.3875
    ma = 296.0
    scaled = (prices-mi) / (ma-mi)
    X_test = np.array(scaled)
    X_test = np.reshape(X_test, (1, X_test.shape[0], 1))
    Prsc = mo41.predict(X_test)
    Pr = Prsc*(ma-mi)+mi
    return Pr 

def PredL(prices):
    mi = 9.685
    ma = 97.06
    scaled = (prices-mi) / (ma-mi)
    X_test = np.array(scaled)
    X_test = np.reshape(X_test, (1, X_test.shape[0], 1))
    Prsc = mo42.predict(X_test)
    Pr = Prsc*(ma-mi)+mi
    return Pr 
""" 
Bitcoin Info:
    Model 40
    Lookback=60 #Amount of Inputs
    Window = 6^+ 1 #Amount of Datapoints to Calc run Mean 
    Outlook = 1 #Amount of Outputs
    
    Trained on 1 week 
    mi=1714.555
    ma=16583.8   
"""
""" 
Ether Info:
    Model 41
    Lookback=60 #Amount of Inputs
    Window = 4 + 2 #Amount of Datapoints to Calc run Mean 
    Outlook = 1 #Amount of Outputs
    
    Trained on 1 week 
    mi=31.3875
    ma=296.0
"""
""" 
Litecoin Info:
    Model 42
    Lookback=60 #Amount of Inputs
    Window = 4 + 2 #Amount of Datapoints to Calc run Mean 
    Outlook = 1 #Amount of Outputs
    
    Trained on 1 week 
    mi=9.685
    ma=97.06
"""