# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 13:42:26 2021

@author: Lionel
This file allows the simulation to run predictions, if they are defined below:
"""

# Source: https://www.kdnuggets.com/2018/11/keras-long-short-term-memory-lstm-model-predict-stock-prices.html

#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
mo40 = load_model("PredModels/model51_2")
mo41 = load_model("PredModels/model50")
mo42 = load_model("PredModels/model52")  


# Prediction function for every coin
# The min Max come from the predictions.py in the data folder and were manually 
# extracted. Important: Make sure Min Max match to trained model and ensure that
# scaling function is the same. Furthermore, input shape and size must match
# the inputs used for training of the model.
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
    Model 51 & 51_2
    Lookback=60 #Amount of Inputs
    Window = 6^+ 1 #Amount of Datapoints to Calc run Mean 
    Outlook = 1 #Amount of Outputs
    
    Trained on 1 week 
    mi=1714.555
    ma=16583.8   
"""
""" 
Ether Info:
    Model 50
    Lookback=60 #Amount of Inputs
    Window = 4 + 2 #Amount of Datapoints to Calc run Mean 
    Outlook = 1 #Amount of Outputs
    
    Trained on 1 week 
    mi=31.3875
    ma=296.0
"""
""" 
Litecoin Info:
    Model 52
    Lookback=60 #Amount of Inputs
    Window = 4 + 2 #Amount of Datapoints to Calc run Mean 
    Outlook = 1 #Amount of Outputs
    
    Trained on 1 week 
    mi=9.685
    ma=97.06
"""