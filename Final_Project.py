from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import yfinance as yf
import matplotlib.pyplot as plt


ticker_list = ['IBM', 'MSFT', 'AAPL', 'AMZN']
# for testing 
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
#from keras.models import Sequential
#from keras.layers import Dense, LSTM



# use this to change the ticker  

 
# Let us  get historical stock prices for Facebook
# covering the past few years.
# max->maximum number of daily prices available
# for Facebook.
# Valid options are 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y,
# 5y, 10y and ytd.

'''     

Convert into plotly figure and use inputs to change ticker and date
'''
GetFacebookInformation = yf.Ticker("FB")
z = GetFacebookInformation.history(period="max")['Close']
# use the period to edit the timeline
plt.figure(figsize=(16,8))
plt.title('History')
plt.plot(z)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price $', fontsize=18)
#plt.show()


data = z




app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.Br(),
    dcc.Dropdown(id='country_dd',
        # Set the available options with noted labels and values
        # stock input 
        options=[{'label':stock, 'value':stock} for stock in ticker_list],
            style={'width':'200px', 'margin':'0 auto'}),
    
    html.Br()
        ])

@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='graph', component_property='figure'),
    Input(component_id='country_dd', component_property='value')
)
def customize_inputs(inputs):
    if inputs == None:
        inputs = 'FB'
    GetFacebookInformation = yf.Ticker(inputs)

    fig = px.line(GetFacebookInformation.history(period="max"), y='Close', template="simple_white", title=f'Date vs. {inputs}')
    return fig


if __name__ == '__main__':
    app.run_server()




