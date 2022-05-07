from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

#SOURCES: https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
#https://towardsdatascience.com/an-interactive-web-dashboard-with-plotly-and-flask-c365cdec5e3f 

df = pd.read_csv(r'code/SentimentAnalysis/sentiment_df.csv')
df = df[['date', 'sentiment', 'compound']]
df2 = pd.DataFrame({
    'Company': [],
    'Date': [],
    'Count Type': [],
    'Count': [],
    'Compound Average': []
})
entry = {'Company': 'Tesla', 'Date': '2022-04-30', 'Count Type': 'Positive', 'Count': df['sentiment'].value_counts()['positive'], 'Compound Average': df['compound'].mean()}
df2 = df2.append(entry, ignore_index = True)
entry = {'Company': 'Tesla', 'Date': '2022-04-30', 'Count Type': 'Negative', 'Count': df['sentiment'].value_counts()['negative'], 'Compound Average': df['compound'].mean()}
df2 = df2.append(entry, ignore_index = True)

#test company
entry = {'Company': 'TestCompany', 'Date': '2022-04-30', 'Count Type': 'Positive', 'Count': 42, 'Compound Average': 0.5}
df2 = df2.append(entry, ignore_index = True)
entry = {'Company': 'TestCompany', 'Date': '2022-04-30', 'Count Type': 'Negative', 'Count': 69, 'Compound Average': 0.5}
df2 = df2.append(entry, ignore_index = True)
entry = {'Company': 'TestCompany', 'Date': '2022-04-29', 'Count Type': 'Positive', 'Count': 42, 'Compound Average': 0.4}
df2 = df2.append(entry, ignore_index = True)
entry = {'Company': 'TestCompany', 'Date': '2022-04-29', 'Count Type': 'Negative', 'Count': 69, 'Compound Average': 0.4}
df2 = df2.append(entry, ignore_index = True)

#test date
entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Positive', 'Count': 0, 'Compound Average': -0.2}
df2 = df2.append(entry, ignore_index = True)
entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Negative', 'Count': 0, 'Compound Average': -0.2}
df2 = df2.append(entry, ignore_index = True)
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
    fig = px.line(df2[df2['Company']==company], x='Date', y='Compound Average', title='Compound Average per Day for One Company')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #return render_template('notdash.html', graphJSON=graphJSON)
    return graphJSON


@app.route('/posnegcount')
def posneg():
    return render_template('notdash.html', graphJSON=callbacktest2())

@app.route('/callbacktest2', methods=['POST', 'GET'])
def cb1():
    return callbacktest2(request.args.get('data'))

def callbacktest2(date = '2022-04-30'):
    fig = px.bar(df2[df2['Date']==date], x='Company', y='Count', color='Count Type', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #return render_template('notdash.html', graphJSON=graphJSON)
    return graphJSON

if __name__ == "__main__":
    app.run()

