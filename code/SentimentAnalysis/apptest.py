from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

#SOURCES: https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
#https://towardsdatascience.com/an-interactive-web-dashboard-with-plotly-and-flask-c365cdec5e3f 

from TwitterScraper import *

def adjustSentimentDataFrame(raw_df, company):
    raw_df = raw_df[['date', 'sentiment', 'compound']]
    
    new_df = pd.DataFrame({
        'Company': [],
        'Date': [],
        'Count Type': [],
        'Count': [],
        'Compound Average': []
    })
    dates = raw_df['date'].drop_duplicates().tolist()
    
    for date in dates:
        temp = raw_df[raw_df['date']==date]
        entry = {'Company': company, 'Date': date, 'Count Type': 'Positive', 'Count': temp['sentiment'].value_counts()['positive'], 'Compound Average': temp['compound'].mean()}
        new_df = new_df.append(entry, ignore_index = True)
        entry = {'Company': company, 'Date': date, 'Count Type': 'Negative', 'Count': temp['sentiment'].value_counts()['negative'], 'Compound Average': temp['compound'].mean()}
        new_df= new_df.append(entry, ignore_index = True)
    return new_df

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    

@app.route('/posnegcount')
def posneg():
    return render_template('positive_negative.html', graphJSON=positiveNegativeCallBackTest())

@app.route('/positiveNegativeCallBackTest', methods=['POST', 'GET'])
def cb1():
    return positiveNegativeCallBackTest(request.args.get('data'))

def positiveNegativeCallBackTest(company = 'Tesla'):
    sentiment_df = scrapeAndCleanse(company)
    sentiment_df = adjustSentimentDataFrame(sentiment_df,company)
    print(sentiment_df)
    
    sentimentTitle = "Overall Twitter Sentiment for {companyName} by Date".format(companyName = company)
    fig = px.bar(sentiment_df[sentiment_df['Company']==company], x='Date', y='Count', color='Count Type', barmode='group',  title=sentimentTitle)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/compavg')
def compavg():
    return render_template('compound_sentiment.html', graphJSON=compoundSentimentCallBackTest())

@app.route('/compoundSentimentCallBackTest', methods=['POST', 'GET'])
def cb():
    return compoundSentimentCallBackTest(request.args.get('data'))

def compoundSentimentCallBackTest(company = 'Tesla'):
    sentiment_df = scrapeAndCleanse(company)
    sentiment_df = adjustSentimentDataFrame(sentiment_df, company)
    print(sentiment_df)
    
    sentimentTitle = "Overall Twitter Sentiment for {companyName} by Date".format(companyName = company)
    fig = px.line(sentiment_df[sentiment_df['Company']==company], x='Date', y='Compound Average', title=sentimentTitle)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == "__main__":
    app.run()
