from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

import tweepy
import datetime 
import os
import re
import sys
import nltk
from dotenv import load_dotenv
load_dotenv()

from SentimentAnalysis import cleanseTweets, scrapeTweets, sentimentAnalyze

def scrape(searchHashtagWord, numTweetsToPull):
    dateFrom = datetime.datetime(2020, 4, 30)
    #Scrape the tweets using the provided hashtag
    twitter_df= scrapeTweets.twitterScraper(searchHashtagWord, numTweetsToPull, dateFrom)

    #Cleanse Tweets
    cleansedDataFrame = cleanseTweets.cleanseTweets(twitter_df)

    #Run Sentiment Analysis on the Tweets
    sentimentDataFrame = sentimentAnalyze.sentimentAnalyze(cleansedDataFrame) 
    sentimentDataFrame['date'] = sentimentDataFrame['date'].map(lambda x: re.sub(r" \d{1,2}:\d{2}:\d{2}\+\d{2}:\d{2}", "", str(x)))
    return sentimentDataFrame

def createdfforapp(df, company):
    df = df[['date', 'sentiment', 'compound']]
    df2 = pd.DataFrame({
        'Company': [],
        'Date': [],
        'Count Type': [],
        'Count': [],
        'Compound Average': []
    })
    dates = df['date'].drop_duplicates().tolist()
    print(dates)
    for date in dates:
        temp = df[df['date']==date]
        entry = {'Company': company, 'Date': date, 'Count Type': 'Positive', 'Count': temp['sentiment'].value_counts()['positive'], 'Compound Average': temp['compound'].mean()}
        df2 = df2.append(entry, ignore_index = True)
        entry = {'Company': company, 'Date': date, 'Count Type': 'Negative', 'Count': temp['sentiment'].value_counts()['negative'], 'Compound Average': temp['compound'].mean()}
        df2 = df2.append(entry, ignore_index = True)
    return df2

#SOURCES: https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
#https://towardsdatascience.com/an-interactive-web-dashboard-with-plotly-and-flask-c365cdec5e3f 

#df = pd.read_csv(r'code/SentimentAnalysis/sentiment_df.csv')
# def createdfforapp(df, company):
#     df = df[['date', 'sentiment', 'compound']]
#     df2 = pd.DataFrame({
#         'Company': [],
#         'Date': [],
#         'Count Type': [],
#         'Count': [],
#         'Compound Average': []
#     })
#     dates = df['date'].drop_duplicates()
#     print(dates)
    # entry = {'Company': 'Tesla', 'Date': '2022-04-30', 'Count Type': 'Positive', 'Count': df['sentiment'].value_counts()['positive'], 'Compound Average': df['compound'].mean()}
    # df2 = df2.append(entry, ignore_index = True)
    # entry = {'Company': 'Tesla', 'Date': '2022-04-30', 'Count Type': 'Negative', 'Count': df['sentiment'].value_counts()['negative'], 'Compound Average': df['compound'].mean()}
    # df2 = df2.append(entry, ignore_index = True)

# #test company
# entry = {'Company': 'TestCompany', 'Date': '2022-04-30', 'Count Type': 'Positive', 'Count': 42, 'Compound Average': 0.5}
# df2 = df2.append(entry, ignore_index = True)
# entry = {'Company': 'TestCompany', 'Date': '2022-04-30', 'Count Type': 'Negative', 'Count': 69, 'Compound Average': 0.5}
# df2 = df2.append(entry, ignore_index = True)
# entry = {'Company': 'TestCompany', 'Date': '2022-04-29', 'Count Type': 'Positive', 'Count': 42, 'Compound Average': 0.4}
# df2 = df2.append(entry, ignore_index = True)
# entry = {'Company': 'TestCompany', 'Date': '2022-04-29', 'Count Type': 'Negative', 'Count': 69, 'Compound Average': 0.4}
# df2 = df2.append(entry, ignore_index = True)

# #test date
# entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Positive', 'Count': 0, 'Compound Average': -0.2}
# df2 = df2.append(entry, ignore_index = True)
# entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Negative', 'Count': 0, 'Compound Average': -0.2}
# df2 = df2.append(entry, ignore_index = True)
#df.loc[df['column_name'] == some_value]

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compavg')
def compavg():
    return render_template('notdash2.html', graphJSON=callbacktest())

@app.route('/callbacktest', methods=['POST', 'GET'])
def cb():
    return callbacktest(request.args.get('data'))

def callbacktest(company = 'Tesla'):
    df = scrape('#' + company, 200)
    df2 = createdfforapp(df,company)
    fig = px.line(df2[df2['Company']==company], x='Date', y='Compound Average', title='Compound Average per Day for One Company')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #return render_template('notdash.html', graphJSON=graphJSON)
    return graphJSON


# df3 = scrape('#Tesla', 200)
# df4 = createdfforapp(df3,'Tesla')
@app.route('/posnegcount')
def posneg():
    return render_template('notdash.html', graphJSON=callbacktest2())

@app.route('/callbacktest2', methods=['POST', 'GET'])
def cb1():
    return callbacktest2(request.args.get('data'))

# def callbacktest2(date = '2022-05-07'):
#     fig = px.bar(df4[df4['Date']==date], x='Company', y='Count', color='Count Type', barmode='group')
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     #return render_template('notdash.html', graphJSON=graphJSON)
#     return graphJSON
def callbacktest2(company = 'Tesla'):
    df3 = scrape('#' + company, 200)
    df4 = createdfforapp(df3,company)
    fig = px.bar(df4[df4['Company']==company], x='Date', y='Count', color='Count Type', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #return render_template('notdash.html', graphJSON=graphJSON)
    return graphJSON

if __name__ == "__main__":
    app.run()

