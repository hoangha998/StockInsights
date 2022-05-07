from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

#df.loc[df['column_name'] == some_value]

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posnegcount')
def posneg():
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

    #test date
    entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Positive', 'Count': 0, 'Compound Average': -0.2}
    df2 = df2.append(entry, ignore_index = True)
    entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Negative', 'Count': 0, 'Compound Average': -0.2}
    df2 = df2.append(entry, ignore_index = True)

    fig = px.bar(df2, x='Company', y='Count', color='Count Type', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('notdash.html', graphJSON=graphJSON)


@app.route('/compavg')
def compavg():
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

    #test date
    entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Positive', 'Count': 0, 'Compound Average': -0.2}
    df2 = df2.append(entry, ignore_index = True)
    entry = {'Company': 'Tesla', 'Date': '2022-04-29', 'Count Type': 'Negative', 'Count': 0, 'Compound Average': -0.2}
    df2 = df2.append(entry, ignore_index = True)

    fig = px.line(df2, x='Date', y='Compound Average', title='Compound Average per Day for One Company')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('notdash.html', graphJSON=graphJSON)


if __name__ == "__main__":
    app.run()

