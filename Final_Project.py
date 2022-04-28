from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from datetime import date, datetime, timedelta
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import yfinance as yf
import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
#from keras.models import Sequential
#from keras.layers import Dense, LSTM

ticker = 'FB'


'''     
Add two more charts one with 40MA and 100MA and the other with tracking trend directions 
Convert into plotly figure and use inputs to change ticker and date
'''
GetFacebookInformation = yf.Ticker("FB")
z = GetFacebookInformation.history(period="max")['Close']
# use the period to edit the timeline



data = z




app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.Br(),
    dcc.Graph(id="graphs"),
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

    stock_data = stock.history(period="max")

    df = pd.DataFrame(stock_data)

    mintime, maxtime = [df.index.min(), df.index.max()]
    df['SMA50'] = df['Close'].rolling(50).mean()
    df['SMA200'] = df['Close'].rolling(200).mean()
    df['SMA40'] = df['Close'].rolling(40).mean()
    df['SMA100'] = df['Close'].rolling(100).mean()
  

    #fig = px.line(df, x=df.index, y='Close', template="simple_white", title=f'{inputs} stock data')
    fig = px.line(df, x=df.index, y=['Close','SMA200','SMA50'], template="simple_white", title=f'{inputs} stock data')
    return fig

@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='graphs', component_property='figure'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')

)
def customize_stock(n_clicks,inputs):
    
    if inputs == None or inputs == '' or n_clicks <= 0:
        inputs = 'FB'
    
    stock = yf.Ticker(inputs)

    stock_data = stock.history(period="max")

    df = pd.DataFrame(stock_data)

    mintime, maxtime = [df.index.min(), df.index.max()]
    df['SMA50'] = df['Close'].rolling(50).mean()
    df['SMA200'] = df['Close'].rolling(200).mean()
    df['SMA40'] = df['Close'].rolling(40).mean()
    df['SMA100'] = df['Close'].rolling(100).mean()
  

    #fig = px.line(df, x=df.index, y='Close', template="simple_white", title=f'{inputs} stock data')
    figs = px.line(df, x=df.index, y=['Close','SMA100','SMA40'], template="simple_white", title=f'{inputs} stock data')
    return figs
    #print(aapl.loc[pd.Timestamp('2006-11-01'):pd.Timestamp('2006-12-31')].______)
#     daily_close = aapl[['Adj Close']]

# # Daily returns
# daily_pct_change = daily_close.pct_change()

# # Replace NA values with 0
# daily_pct_change.fillna(0, inplace=True)

# # Inspect daily returns
# print(daily_pct_change)

# # Daily log returns
# daily_log_returns = np.log(daily_close.pct_change()+1)


# import matplotlib.pyplot as plt 

# # Define the minumum of periods to consider 
# min_periods = 75 

# # Calculate the volatility
# vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods) 

# # Plot the volatility
# vol.plot(figsize=(10, 8))
if __name__ == '__main__':
    app.run_server()




