from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from datetime import date, datetime, timedelta
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt



# for testing 
import math
from sklearn.preprocessing import MinMaxScaler
#from keras.models import Sequential
#from keras.layers import Dense, LSTM

ticker = 'FB'

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

df = px.data.stocks()
print(df.head())


data = z




app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.Br(),
    dcc.Textarea(
        id='textarea-state-example',
        value='',
        style={'width': '10%', 'height': 25,  'align': 'center'},
    ),
    html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
    html.Br(),
    html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'}),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=datetime.now() - timedelta(days=3*365),
        max_date_allowed= datetime.now(),
        
    
    ),
    html.Div(id='output-container-date-picker-range'),
    # dcc.Dropdown(id='country_dd',
    #     # Set the available options with noted labels and values
    #     # stock input 
    #     options=[{'label':stock, 'value':stock} for stock in ticker_list],
    #         style={'width':'200px', 'margin':'0 auto'}),
    
    html.Br()
        ])

# @app.callback(
#     Output(component_id='graph', component_property='figure'),
#     Input('my-date-picker-range','start_date'),
#     Input('my-date-picker-range','end_date'),

# )
# def update(start_date,end_date):
#     print(start_date, end_date)
# #     startDate = datetime(start_date)
 
# # # endDate , as per our convenience we can modify
# #     endDate = datetime(end_date)
#     Information = yf.Ticker(ticker)
 
# # pass the parameters as the taken dates for start and end
#     df = Information.history(start = start_date, end = end_date)
#     fig = px.line(df, x=df.index, y='Close', template="simple_white", title=f'{ticker} stock data')
#     return fig



@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='graph', component_property='figure'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')

)
def customize_inputs(n_clicks,inputs):
    
    if inputs == None or inputs == '' or n_clicks <= 0:
        inputs = 'FB'
    
    stock = yf.Ticker(inputs)
      # Company name
# get last 5 years of data
    '''
    nio = yf.Ticker('inputs')
    history = nio.history(period="Max")
    df = pd.DataFrame(history)
    df.reset_index(inplace=True)
    df['date'] = pd.to_datetime(df.date)
    x = df[['Open', 'High','Low', 'Volume']]
    y = df['Close']

    ''' 
    stock_data = stock.history(period="max")

    df = pd.DataFrame(stock_data)
    df['SMA50'] = df['Close'].rolling(50).mean()
    df['SMA200'] = df['Close'].rolling(200).mean()


    time = [df.index.min(), df.index.max()]


    fig = px.line(df, x=df.index, y=['Close','SMA200','SMA50'], template="simple_white", title=f'{inputs} stock data')
    return fig


if __name__ == '__main__':
    app.run_server()




