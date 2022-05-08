""" python file to create methods to calculate KPI's """
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt

if __name__ == "__main__":
    tickers = ["MSFT", "FB", "AMZN", "GOOG", "TSLA"]
    start = dt.datetime.today() - dt.timedelta(365)
    end = dt.datetime.today()
    close_price = (
        pd.DataFrame()
    )  # empty dataframe which will be filled with closing prices of each stock

    # looping over tickers and creating a dataframe with close prices
    for ticker in tickers:
        close_price[ticker] = yf.download(ticker, start, end)["Adj Close"]

    # dropping NaN values
    close_price.dropna(axis=0, how="any", inplace=True)

    print(close_price.describe())

