
#%%
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

btcData = pd.read_csv("Data/Bitcoin_Min_Jan20.csv")
ethData = pd.read_csv("Data/Ether_Min_Jan20.csv")
ltcData = pd.read_csv("Data/Lite_Min_Jan20.csv")
summaryData = pd.read_csv("summary.csv")
#print(summaryData)
dim = summaryData.shape[0]

#%%
buffer= 24*60*7 #1 Week data to use for models

#%% live plotting with dash
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
                    range=[min(X),max(X)]),yaxis = 
                    dict(range = [min(Y),max(Y)]),
                    )}
# %% 
if __name__ == '__main__':
    #app.run_server()
    bitcoin_candelstick = go.Figure(data=[go.Candlestick(
    x=btcData['time_period_start'],
    open=btcData['price_open'], high=btcData['price_high'],
    low=btcData['price_low'], close=btcData['price_close'],
    increasing_line_color= 'cyan', decreasing_line_color= 'gray'
)])

bitcoin_candelstick.show()

ethereum_candelstick = go.Figure(data=[go.Candlestick(
    x=ethData['time_period_start'],
    open=ethData['price_open'], high=ethData['price_high'],
    low=ethData['price_low'], close=ethData['price_close'],
    increasing_line_color= 'lime', decreasing_line_color= 'gray'
)])

ethereum_candelstick.show()

litecoin_candelstick = go.Figure(data=[go.Candlestick(
    x=ltcData['time_period_start'],
    open=ltcData['price_open'], high=ltcData['price_high'],
    low=ltcData['price_low'], close=ltcData['price_close'],
    increasing_line_color= 'papayawhip', decreasing_line_color= 'gray'
)])

litecoin_candelstick.show()


# %%

def Plotter(Sum,buffer,dfBTC,dfETH,dfLTC,RSI_Trader,Adv_Trader,Hill_Trader,Jack_Trader,Tiered_Trader,Loser_Trader,Random_Trader,Insider_Trader,Shuffle_Trader):
    #%% Figure 1: 3 Coins Comparison, Coin Values in Dollars  

    
    base = dt.date(2020, 1, 1)
    dim=min([dfBTC.shape[0],dfETH.shape[0],dfLTC.shape[0]])
    horizon=dim-buffer
    arr = list([base + dt.timedelta(weeks=i) for i in range(5)])
    tik = list([-buffer, 0, buffer, 2*buffer, 3*buffer])    
    Mins=np.array(list(range(0,horizon)))
    ng=np.array(list(range(-buffer,0)))
    

    fig, axs = plt.subplots(3, sharex=True, sharey=False)
    plt.setp(axs, xticks=tik, xticklabels=arr)
    plt.subplots_adjust(hspace=0.5)
    fig.suptitle('Coin Performance January 2020')

    axs[0].plot(ng,dfBTC.iloc[0:buffer,8])
    axs[0].plot(Mins,dfBTC.iloc[buffer:dim,8])
    axs[0].set_title('Bitcoin')
    axs[0].vlines(0,min(dfBTC.iloc[0:dim,8]),max(dfBTC.iloc[0:dim,8]),colors='k',linestyles='dashed')
    
    
    axs[1].plot(ng,dfETH.iloc[0:buffer,8])
    axs[1].plot(Mins,dfETH.iloc[buffer:dim,8])
    axs[1].set_title('Ethereum')
    axs[1].set_ylabel('Dollar Value')
    axs[1].vlines(0,min(dfETH.iloc[0:dim,8]),max(dfETH.iloc[0:dim,8]),colors='k',linestyles='dashed')
    
    
    axs[2].plot(ng,dfLTC.iloc[0:buffer,8])
    axs[2].plot(Mins,dfLTC.iloc[buffer:dim,8])
    axs[2].set_title('Litecoin')
    axs[2].set_xlabel('Time')
    axs[2].vlines(0,min(dfLTC.iloc[0:dim,8]),max(dfLTC.iloc[0:dim,8]),colors='k',linestyles='dashed')
   
    fig.show()    
    
    #%% Figure 2:
        
    fig2 = plt.figure()
    for i in range(1,10):
        plt.plot(Sum.table.iloc[:,0],Sum.table.iloc[:,i])
    plt.legend(['Rule Trader', 'Advanced Trader', 'Up-Down Trader', 'Jacks Trader', 'Tiered Trader','Random Trader','Losing Trader','Insider Trader','Insider Trader','Emotional Trader'])
    plt.title('Trader Performance January 2020')
    fig2.show()
    
    return

def Analyze(Sum,dfBTC,dfETH,dfLTC,RSI_Trader,Adv_Trader,Hill_Trader,Jack_Trader,Tiered_Trader,Loser_Trader,Random_Trader):
    # Get info about total trades
    # Get info about optimal trades
    # Get info about anything else you migth be interested in.
    return