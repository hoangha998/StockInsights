import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import yfinance as yf
import matplotlib.pyplot as plt


ticker_list = ['IBM', 'MSFT', 'AAPL', 'AMZN']
# for testing 
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM



# use this to change the ticker  
GetFacebookInformation = yf.Ticker("FB")
 
# Let us  get historical stock prices for Facebook
# covering the past few years.
# max->maximum number of daily prices available
# for Facebook.
# Valid options are 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y,
# 5y, 10y and ytd.

'''     

Convert into plotly figure and use inputs to change ticker and date
'''

print(GetFacebookInformation.history(period="max"))
# use the period to edit the timeline
plt.figure(figsize=(16,8))
plt.title('History')
plt.plot(GetFacebookInformation['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price $', fontsize=18)
plt.show()


data = GetFacebookInformation.filter(['Close'])
dataset = data.values
training_data_len = math.ceil(len(dataset) * .8)
training_data_len

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)
scaled_data

# use train_split_form
train_data = scaled_data[0:training_data_len , :]
x_train = []
y_train = []
for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])
  if i<=61:
    print(x_train)
    print(y_train)
    print()



app = dash.Dash(__name__)




if __name__ == '__main__':
    app.run_server()