from dash import Dash, html, dcc
import plotly.express as px
import plotly.express as px
import pandas as pd
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
stock = yf.Ticker('FB')

stock_data = stock.history(period="max")

df = pd.DataFrame(stock_data)
ecom_sales = pd.DataFrame(stock_data)
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'
ecom_scatter = px.line(ecom_sales, x=ecom_sales.index, y='Close', width=850, height=550)
ecom_scatter.update_layout({'legend':dict(orientation='h', y=-0.7,x=1, yanchor='bottom', xanchor='right')})

app = Dash(__name__)

app.layout = html.Div([
  html.Img(src=logo_link, 
        style={'margin':'30px 0px 0px 0px' }),
  html.H1('Sales breakdowns'),
  html.Div(
    children=[
    html.Div(
        children=[
          html.H3('Sales Volume vs Sales Amount by Country'),
          dcc.Graph(id='scatter'),
        ],
        style={'width':'950px', 'height':'650px', 'display':'inline-block', 
               'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'}),    
    html.Br(),
    dcc.Textarea(
        id='textarea-state-example',
        value='',
        style={'width': '10%', 'height': 25,  'align': 'center'},
    ),
    html.Button('Submit', id='textarea-state-example-button', n_clicks=0, style={'height': 25}),
    html.Br(),
    
    html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'}),
    html.Div(
      children=[
        dcc.Graph(id='major_cat'),
        dcc.Graph(id='minor_cat'),
      ],
      style={'width':'1250px', 'height':'625px','display':'inline-block'})
    ]),], 
  style={'text-align':'center', 'display':'inline-block', 'width':'100%'}
  )
@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='scatter', component_property='figure'),
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

  

    #fig = px.line(df, x=df.index, y='Close', template="simple_white", title=f'{inputs} stock data')
    fig = px.line(df, x=df.index, y='Close', template="simple_white", title=f'{inputs} stock data')
    return fig
@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='major_cat', component_property='figure'),
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

  

    #fig = px.line(df, x=df.index, y='Close', template="simple_white", title=f'{inputs} stock data')
    fig = px.line(df, x=df.index, y=['Close','SMA200','SMA50'], template="simple_white", title=f'{inputs} stock data', width=900, height=500)
    return fig

@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='minor_cat', component_property='figure'),
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

    df['SMA40'] = df['Close'].rolling(40).mean()
    df['SMA100'] = df['Close'].rolling(100).mean()
  

    #fig = px.line(df, x=df.index, y='Close', template="simple_white", title=f'{inputs} stock data')
    figs = px.line(df, x=df.index, y=['Close','SMA100','SMA40'], template="simple_white", title=f'{inputs} stock data', width=900, height=500)
    return figs
# @app.callback(
#     Output('major_cat', 'figure'),
#     Input('scatter', 'hoverData'))

# def update_major_cat_hover(hoverData):
#     hover_country = 'Australia'
    
#     if hoverData:
#         hover_country = hoverData['points'][0]['customdata'][0]

#     major_cat_df = ecom_sales[ecom_sales['Country'] == hover_country]
#     major_cat_agg = major_cat_df.groupby('Major Category')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')

#     ecom_bar_major_cat = px.bar(major_cat_agg, x='Total Sales ($)',
#                                 # Ensure the Major category will be available
#                                 custom_data=['Major Category'],
#                                 y='Major Category', height=300, 
#                                 title=f'Sales by Major Category for: {hover_country}', color='Major Category',
#             color_discrete_map={'Clothes':'blue','Kitchen':'red', 'Garden':'green', 'Household':'yellow'})
#     ecom_bar_major_cat.update_layout({'margin':dict(l=10,r=15,t=40,b=0), 'title':{'x':0.5}})

#     return ecom_bar_major_cat

# # Set up a callback for click data
# @app.callback(
#     Output('minor_cat', 'figure'),
#     Input('major_cat', 'clickData'))

# def update_major_cat_click(clickData):
#     click_cat = 'All'
#     major_cat_df = ecom_sales.copy()
#     total_sales = major_cat_df.groupby('Country')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    
#     # Extract the major category clicked on for usage
#     if clickData:
#         click_cat = clickData['points'][0]['customdata'][0]
        
#         # Undetake a filter using the major category clicked on
#         major_cat_df = ecom_sales[ecom_sales['Major Category'] == click_cat]
    
#     country_mj_cat_agg = major_cat_df.groupby('Country')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
#     country_mj_cat_agg['Sales %'] = (country_mj_cat_agg['Total Sales ($)'] / total_sales['Total Sales ($)'] * 100).round(1)
    
#     ecom_bar_country_mj_cat = px.bar(country_mj_cat_agg, x='Sales %', y='Country', 
#                                 orientation='h', height=450, range_x = [0,100], text='Sales %', 
#                                      title=f'Global Sales % by Country for Major Category: {click_cat}')
#     ecom_bar_country_mj_cat.update_layout({'yaxis':{'dtick':1, 'categoryorder':'total ascending'}, 'title':{'x':0.5}})

#     return ecom_bar_country_mj_cat
  

if __name__ == '__main__':
    app.run_server(debug=True,port=3004)