#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, flash, request, redirect, url_for, jsonify, \
    render_template, Response

# hoang's imports

from group_code.TradingStyles.dash_app import get_dash_app
from group_code.NeuralNetwork.Predictor import TrendPredictor

# john's imports

from posixpath import split
from textwrap import indent
from cProfile import label
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt
import json

app = Flask(__name__)

# initialize trend predictor
# trend_predictor = TrendPredictor() DON'T DELETE
trend_predictor = None

# intialize dash app

dash_app = get_dash_app(app)


@app.route('/')
def index():
    return render_template('README.html')


@app.route('/trend_prediction', methods=['GET', 'POST'])
def trend_prediction():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        print 'new ticker ({}) requested..'.format(ticker)
        trend_predictor.set_ticker(ticker)
        (decrease, increase, same) = trend_predictor.predict()
        increase = '{:.2f}'.format(increase * 100)
        decrease = '{:.2f}'.format(decrease * 100)
        same = '{:.2f}'.format(same * 100)
        result = {
            'ticker': ticker,
            'increase_confidence': increase,
            'decrease_confidence': decrease,
            'same_confidence': same,
            }
        return render_template('trend_prediction.html', result=result)

    return render_template('trend_prediction.html', result=False)


@app.route('/Andrew')
def andrew():
    variable = 100
    return render_template('andrew.html', number=variable)


@app.route('/Zach')
def zach():
    return render_template('zach.html')


@app.route('/keith')
def keith():
    # from code import TradingStyles
    return dash_app.index()


# use html template to show form with input for ticker, start date, and end date

@app.route('/john', methods=['GET'])
def john():
    return render_template('john.html')


# post route to use yfinance to get data

@app.route('/data', methods=['POST'])
def getData():
    if request.method == 'POST':
        data = request.json
        close_price = pd.DataFrame()
        close_price[data['ticker']] = yf.download(data['ticker'],
                data['startDate'], data['endDate'])['Adj Close']
        stockStats = close_price.describe()
        temp_dict = dict()
        for (i, row) in stockStats.iterrows():
            temp_dict[row.name] = row.values[0]
        theJSON = close_price.to_json(date_format='iso', orient='split')
        temp_json = json.loads(theJSON)
        temp_json.update(temp_dict)

        # print(temp_json)
        # return close_price.to_json(date_format="iso")

        return temp_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
