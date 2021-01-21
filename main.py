import pandas as pd
import datetime
import math
import csv  

from Classes import trader 
from Classes import market


df = pd.read_csv ("Bitcoin_Min_Jan20.csv")
dim=df.shape[0]

buffer=24*60*14 #amount of minutes before t0 we use for preds at t0

for t in range (buffer,dim):
    market.close= df.iloc[t,8]
    #This is Simulating time
    
    #Call Prediciton function
    #Call trader 
    #etc
    t=+1
    


#df.columns
# def main():
#     tr1 = trader(100000, "ETH")
#     print("trader owns " + tr1.portfolio + " and $" + str(tr1.bank) + " left in the bank")

#     m1 = market("AAPL", "1/19/2021", market.getMarketPrice)
#     print("market price for " + m1.ticker + " on " + m1.date + " is " + str(m1.price))
# if __name__ == "__main__":
#     main()
    