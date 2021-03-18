'''
This file was meant to visualize the simulation in it's process. However, due
to time constraints and compatibility issues, it is now solely used to visualize
the results of the simulation AFTER it has been completed. In any case, the code
for live plotting is still included as we felt it would have been a waste to 
delete it
'''
#%%
#Import Libraries
import pandas as pd
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

#Download raw data and the summary
btcData = pd.read_csv("Data/Bitcoin_Min_Jan20.csv")
ethData = pd.read_csv("Data/Ether_Min_Jan20.csv")
ltcData = pd.read_csv("Data/Lite_Min_Jan20.csv")
summaryData = pd.read_csv("summary2.csv")
#print(summaryData)
#dim = summaryData.shape[0]

#%%
buffer= 24*60*7 #1 Week data to use for models

#%% live plotting with dash
'''
X = deque(maxlen = 20)
X.append(1)

Y = deque(maxlen = 20)
Y.append(1)
app = dash.Dash(__name__)
app.layout = html.Div(
    [    
        dcc.Graph(id = 'live-graph',
                  animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 1000,
            n_intervals = 0
        ),
    ]
)

@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
    for t in range (buffer, dim):

        X.append(t)
        Y.append(summaryData.iloc[t,3])

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
    )
    
    print(list(X))
    print(list(Y))
    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(
                    range=[0,40000]),yaxis = 
                    dict(range = [0,4000]),
                    )}
'''
# %% 
#if __name__ == '__main__':
    #app.run_server()
#     bitcoin_candelstick = go.Figure(data=[go.Candlestick(
#     x=btcData['time_period_start'],
#     open=btcData['price_open'], high=btcData['price_high'],
#     low=btcData['price_low'], close=btcData['price_close'],
#     increasing_line_color= 'cyan', decreasing_line_color= 'gray'
# )])

# bitcoin_candelstick.show()

# ethereum_candelstick = go.Figure(data=[go.Candlestick(
#     x=ethData['time_period_start'],
#     open=ethData['price_open'], high=ethData['price_high'],
#     low=ethData['price_low'], close=ethData['price_close'],
#     increasing_line_color= 'lime', decreasing_line_color= 'gray'
# )])

# ethereum_candelstick.show()

# litecoin_candelstick = go.Figure(data=[go.Candlestick(
#     x=ltcData['time_period_start'],
#     open=ltcData['price_open'], high=ltcData['price_high'],
#     low=ltcData['price_low'], close=ltcData['price_close'],
#     increasing_line_color= 'papayawhip', decreasing_line_color= 'gray'
# )])

# litecoin_candelstick.show()


# %%
#This function visualizes various aspects of the simulation:
def Plotter(Sum,buffer,dfBTC,dfETH,dfLTC,RSI_Trader,Adv_Trader,Hill_Trader,Variable_Trader,Tiered_Trader,AntiRSI_Trader,Random_Trader,Pred_Trader,Insider_Trader,Shuffle_Trader):
    
    #Figure 1: 3 Coins Comparison, Coin Values in Dollars  
    base = dt.date(2020, 1, 1)
    dim=min([dfBTC.shape[0],dfETH.shape[0],dfLTC.shape[0]])
    horizon=dim-buffer
    arr = list([base + dt.timedelta(weeks=i) for i in range(5)])
    tik = list([-buffer, 0, buffer, 2*buffer, 3*buffer])    
    Mins=np.array(list(range(0,horizon)))
    ng=np.array(list(range(-buffer,0)))
    
    # Create Subplot with 3 figures
    fig, axs = plt.subplots(3, sharex=True, sharey=False)
    plt.setp(axs, xticks=tik, xticklabels=arr)
    plt.subplots_adjust(hspace=0.5)
    fig.suptitle('Coin Performance January 2020')
    #Fig 1: Bitcoin Performance
    axs[0].plot(ng,dfBTC.iloc[0:buffer,8])
    axs[0].plot(Mins,dfBTC.iloc[buffer:dim,8])
    axs[0].set_title('Bitcoin')
    axs[0].vlines(0,min(dfBTC.iloc[0:dim,8]),max(dfBTC.iloc[0:dim,8]),colors='k',linestyles='dashed')
    #Fig 2: Ethereum Performance    
    axs[1].plot(ng,dfETH.iloc[0:buffer,8])
    axs[1].plot(Mins,dfETH.iloc[buffer:dim,8])
    axs[1].set_title('Ethereum')
    axs[1].set_ylabel('Dollar Value')
    axs[1].vlines(0,min(dfETH.iloc[0:dim,8]),max(dfETH.iloc[0:dim,8]),colors='k',linestyles='dashed')
    #Fig 3: Litecoin Performance    
    axs[2].plot(ng,dfLTC.iloc[0:buffer,8])
    axs[2].plot(Mins,dfLTC.iloc[buffer:dim,8])
    axs[2].set_title('Litecoin')
    axs[2].set_xlabel('Time')
    axs[2].vlines(0,min(dfLTC.iloc[0:dim,8]),max(dfLTC.iloc[0:dim,8]),colors='k',linestyles='dashed')
    #Output figure, and Save it in the figures folder.
    fig.show()    
    plt.savefig('./Figures/Coin_Performance_January_2020.pdf')
    
    # Figure 2: Total worth of a trader at every timepoint  
    fig2 = plt.figure()
    for i in range(1,11):
        plt.plot(Sum.table.iloc[:,0],Sum.table.iloc[:,i])
    plt.legend(['Rule Trader','Advanced Trader','Momentum Trader','Variable Trader','Tiered Trader','Anti RSI Trader','Random Trader','Prediction Trader','Insider Trader','Shuffle Trader'],loc="upper left", bbox_to_anchor=(1,1))
    plt.title('Trader Performance January 2020')
    fig2.show()
    plt.savefig('./Figures/Trader_Performance_January_2020.pdf')
    
    return
#%%
def Analyze(Sum,buffer,dfBTC,dfETH,dfLTC,trader,name):
    #This function tries to shine some light into the traders activity in the
    #course of the simulation.
    base = dt.date(2020, 1, 7)
    dim=min([dfBTC.shape[0],dfETH.shape[0],dfLTC.shape[0]])
    horizon=dim-buffer
    arr = list([base + dt.timedelta(weeks=i) for i in range(4)])
    tik = list([buffer, 2*buffer, 3*buffer,4*buffer])   
    prices=np.zeros([Sum.table.shape[0],3])
    totBuys=np.zeros([3])
    Buy=np.zeros([3])
    totSells=np.zeros([3])
    posSells=np.zeros([3])
    negSells=np.zeros([3])
    dif=np.zeros([Sum.table.shape[0],3])
    tsell=np.zeros([1,3])
    tbuy=np.zeros([1,3])
    for i in range (0,Sum.table.shape[0]):
        prices[i,0]=dfBTC.iloc[buffer+i,8]
        prices[i,1]=dfETH.iloc[buffer+i,8]
        prices[i,2]=dfLTC.iloc[buffer+i,8]
        if any (trader.transactions.iloc[i,6:9]==1): #See if we bought
            for j in range(0,3):
                if trader.transactions.iloc[i,6+j]== 1: #If we bought: Save the decision,
                #Save the buying price for later comparison
                    totBuys[j]=totBuys[j]+1
                    Buy[j]=prices[i,j]
                    tbuy[np.int(totBuys[j]-1),j]=buffer+i
                    tbuy=np.append(tbuy,np.zeros([1,3]),axis=0)
        if any (trader.transactions.iloc[i,6:9]==-1): #See if we sold
            for j in range(0,3):
                if trader.transactions.iloc[i,6+j]==-1: #If we sold: Save the decision,
                #Compare Selling price to buying and make conclusions
                    totSells[j]=totSells[j]+1
                    tsell[np.int(totSells[j]-1),j]=buffer+i
                    tsell=np.append(tsell,np.zeros([1,3]),axis=0)
                    dif[i,j]=prices[i,j]-Buy[j] #Calculate difference
                    if prices[i,j] >= Buy[j]: #If we sell higher than we bought, good trade
                        posSells[j]=posSells[j]+1
                    else:
                        negSells[j]=negSells[j]+1
    trader.totBuys=totBuys
    trader.totSells=totSells
    trader.posSells=posSells
    trader.negSells=negSells
    trader.dif=dif
    trader.tsell=tsell
    trader.tbuy=tbuy
    
    #Now visualizing these decisions for every trader and every coin and save the 
    #figure under the name provided to the function from the main file (configured
    #in a way to be saved in the figures folder when left as is.)
    fig1, axs1 = plt.subplots(3, sharex=True, sharey=False)
    plt.setp(axs1, xticks=tik, xticklabels=arr)
    plt.subplots_adjust(hspace=0.5)
    fig1.suptitle('Trader Perfomance Depending on Cryptocurrency')
    
    axs1[0].plot(Sum.table.iloc[:,0], dfBTC.iloc[buffer:,8])
    axs1[0].plot(tbuy[0:np.int(totBuys[0]),0],dfBTC.iloc[tbuy[0:np.int(totBuys[0]),0],8],'r.')
    axs1[0].plot(tsell[0:np.int(totSells[0]),0],dfBTC.iloc[tsell[0:np.int(totSells[0]),0],8],'g.')
    axs1[0].set_title('Bitcoin Trading')

    axs1[1].plot(Sum.table.iloc[:,0], dfETH.iloc[buffer:,8])
    axs1[1].plot(tbuy[0:np.int(totBuys[1]),1],dfETH.iloc[tbuy[0:np.int(totBuys[1]),1],8],'r.')
    axs1[1].plot(tsell[0:np.int(totSells[1]),1],dfETH.iloc[tsell[0:np.int(totSells[1]),1],8],'g.')
    axs1[1].set_title('Ethereum Trading')
    axs1[1].set_ylabel('Dollar Amount')
    
    axs1[2].plot(Sum.table.iloc[:,0], dfLTC.iloc[buffer:,8])
    axs1[2].plot(tbuy[0:np.int(totBuys[2]),2],dfLTC.iloc[tbuy[0:np.int(totBuys[2]),2],8],'r.')
    axs1[2].plot(tsell[0:np.int(totSells[2]),2],dfLTC.iloc[tsell[0:np.int(totSells[2]),2],8],'g.')
    axs1[2].set_title('Litecoin Trading')
    axs1[2].set_xlabel('Time')
    fig1.show()    
    plt.savefig(name)
    return trader.totBuys, trader.totSells, trader.posSells, trader.negSells, trader.dif, trader.tsell, trader.tbuy

