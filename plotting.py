
#%%
import pandas as pd
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque


btcData = pd.read_csv("Data/Bitcoin_Min_Jan20.csv")
summaryData = pd.read_csv("summary.csv")
#%%
buffer= 24*60*7 #1 Week data to use for models

#%% live plotting with dash
X = deque(maxlen = 1000)
X.append(1)

Y = deque(maxlen = 1000)
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
    for t in range (buffer,buffer + 50):

        X.append(X[-1]+t)
        Y.append(Y[-1]+ btcData.iloc[t,8])

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
                    range=[buffer,max(X)]),yaxis = 
                    dict(range = [min(Y),max(Y)]),
                    )}

if __name__ == '__main__':
    app.run_server()

# %%