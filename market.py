import pandas as pd

#Market and trader objects from
from Classes import trader 
from Classes import market

#stock market compoonent of trading model

#handles collecting order and processing selling / buying of stocks

stockPrice = 0


bitData = pd.read_csv ("Bitcoin_Min_Jan20.csv")

def getStockPrice(date):
    infoAtDate = list(bitData.loc[bitData['time_period_start'] == date])
    print(infoAtDate)
    stockPrice = infoAtDate[5]
    print(str(stockPrice))

    
def getStockOrder (n, order):
    #let order be value 1, 0, -1
    #let n be int for number of shares
    if order == 0:
        print("Trader is holding")
    if order == 1:
        print("Trader is buying")
    if order == -1:
        print("Trader is selling")

getStockOrder(1, 1)
getStockPrice('2020-01-01T00:00:00.0000000Z')