from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

from TwitterScraper import *

#SOURCES: https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
#https://towardsdatascience.com/an-interactive-web-dashboard-with-plotly-and-flask-c365cdec5e3f 


#test date
#entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Positive', 'Count': 0, 'Compound Average': -0.2}
#df2 = df2.append(entry, ignore_index = True)
#entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Negative', 'Count': 0, 'Compound Average': -0.2}
#df2 = df2.append(entry, ignore_index = True)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posnegcount')
def posneg():
    print("first")
    #return render_template('compound_average.html', graphJSON=compoundAverageCallbackTest())
    return render_template('positive_negative.html', graphJSON=positiveNegativeCallbackTest())

@app.route('/positiveNegativeCallbackTest1', methods=['POST', 'GET'])
def cb1():
    company = request.args.get('data')
    compoundSentiment_df = scrapeAndCleanse(company)
    
    #Remove unnecessary columns from dataframe
    compoundSentiment_df.drop('text', axis=1, inplace=True)
    compoundSentiment_df.drop('neg', axis=1, inplace=True)
    compoundSentiment_df.drop('neu', axis=1, inplace=True)
    compoundSentiment_df.drop('pos', axis=1, inplace=True)
    compoundSentiment_df.drop('compound', axis=1, inplace=True)
    
    compoundSentiment_df['Company'] = company
    print(compoundSentiment_df)
    return 
    
    
    #return positiveNegativeCallbackTest(request.args.get('data'))

@app.route('/positiveNegativeCallbackTest2', methods=['POST', 'GET'])
def cb2():
    print("wow")
    return compoundAverageCallbackTest(request.args.get('data'))

def positiveNegativeCallbackTest(date = '2022-04-30'):
    print('yes')
    #fig = px.bar(df2[df2['Date']==date], x='Company', y='Count', color='Count Type', barmode='group')
    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #return render_template('notdash.html', graphJSON=graphJSON)
    #return graphJSON
    return "Hello"
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/compavg')
def compavg():
    return render_template('compound_average.html', graphJSON=compoundAverageCallbackTest())
       
@app.route('/compoundAverageCallbackTest', methods=['POST', 'GET'])
def cb():
    print("cb")
    return compoundAverageCallbackTest(request.args.get('data'))

def compoundAverageCallbackTest(company = 'Tesla'):
    compoundSentiment_df = scrapeAndCleanse(company)
    
    #Remove unnecessary columns from dataframe
    compoundSentiment_df.drop('text', axis=1, inplace=True)
    compoundSentiment_df.drop('sentiment', axis=1, inplace=True)
    compoundSentiment_df.drop('neg', axis=1, inplace=True)
    compoundSentiment_df.drop('neu', axis=1, inplace=True)
    compoundSentiment_df.drop('pos', axis=1, inplace=True)
    
    #Calculate Compound Sentiment for each day
    compoundSentiment_df = compoundSentiment_df.groupby('date')['compound'].mean()
    compoundSentiment_df = compoundSentiment_df.to_frame().reset_index()
    
    compoundSentiment_df.set_axis(["Date", "Compound Sentiment" ], axis=1, inplace=True)
    compoundSentiment_df['Company'] = company
    
    sentimentTitle = "Overall Twitter Sentiment for {companyName} by Date".format(companyName = company)
    fig = px.line(compoundSentiment_df[compoundSentiment_df['Company']==company], x='Date', y='Compound Sentiment', title=sentimentTitle)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == "__main__":
    app.run()

