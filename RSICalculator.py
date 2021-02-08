import datetime as dt
import pandas as pd
import math
import csv  
import numpy as np
from datetime import timedelta

from Classes import market


dfBTC = pd.read_csv("Data/Bitcoin_Day_1820.csv")
dfETH = pd.read_csv("Data/Ether_Day_1820.csv")

rsp1 = 14
delta = timedelta(days=rsp1)

# will be today = dt.date.today()
today = dt.date(2020,9,5)

dates = dfBTC.iloc[:,1]
dfBTCdates = pd.read_csv("Data/Bitcoin_Day_1820.csv", index_col="time_period_start", parse_dates=True, usecols=['time_period_start','price_open','price_close'])
fourteendays = today - delta
getfourteendays = dfBTCdates.loc[fourteendays:today]
getfourteendays["difference"] = getfourteendays["price_close"] - getfourteendays["price_open"]
dim = getfourteendays.shape[0]
var1 = getfourteendays["difference"]/getfourteendays["price_open"]

#def rsiINIT(dataframe, Delta, rsperiod, date):

gain = 0
loss = 0
for i in range(0,dim-1):
    if var1.iloc[i] > 0:
        gain = gain + var1.iloc[i]
    else:
        loss = loss - var1.iloc[i]
rs = gain/loss
rsi = 100-(100/(1+rs))
print("gain =", gain)
print("loss =", loss)
print("rsi =", rsi)

def rsi_t(gain_prev,loss_prev,rsi_period,prices):
    runningdiff = (prices["price_close"] - prices["price_open"]) / prices["price_open"]
    if runningdiff > 0:
        rsi = 100-((100)/(1+(((gain_prev*(rsi_period-1))+runningdiff)/((1*loss_prev*(rsi_period-1)+0)))))
    else:
        rsi = 100-((100)/(1+(((gain_prev*(rsi_period-1))+0)/((1*loss_prev*(rsi_period-1)+runningdiff)))))
    return rsi, runningdiff


import cgitb
import cgi
cgitb.enable()
form = cgi.FieldStorage()

coin = form.getvalue('coindropdown')
coin = (form['coindropdown'].value)
header = "Content-Type: text/html\n\n"
output = html.format(result = gain)
print (header)
print (output)