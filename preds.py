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



mo6 = load_model('PredModels/model16/')


#Scaling Factors: Same as Used in Training!
# def Pred16(prices,mo16):
#     mi = 31.8575
#     ma = 269.22
#     scaled = (prices-mi) / (ma-mi)
#     # Pr = mod16.predict(scaled)
#     # return Pr


