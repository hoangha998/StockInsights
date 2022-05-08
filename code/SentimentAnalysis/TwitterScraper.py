import pandas as pd
import tweepy
import datetime 
import os
from dotenv import load_dotenv
load_dotenv()

from cleanseTweets import *
from scrapeTweets import *
from sentimentAnalyze import *




def scrape(searchHashtagWord, numTweetsToPull):
    dateFrom = datetime.datetime(2020, 4, 30)
    #Scrape the tweets using the provided hashtag
    twitter_df= twitterScraper(searchHashtagWord, numTweetsToPull, dateFrom)

    #For Testing Purpose(Save physical df locally)
    #filename = 'raw_tweets.csv'
    #twitter_df.to_csv(filename)

    #For Testing Purpose(Read from local df)
    #rawDataFrame = pd.read_csv("test_tweet.csv")
    #rawDataFrame = pd.read_csv(r"code/SentimentAnalysis/raw_tweets.csv")
    print(twitter_df)

    #Cleanse Tweets
    cleansedDataFrame = cleanseTweets(twitter_df)
    #cleansedDataFrame.to_csv("cleansed_df.csv")

    #Run Sentiment Analysis on the Tweets
    sentimentDataFrame = sentimentAnalyze(cleansedDataFrame) 
    sentimentDataFrame['date'] = sentimentDataFrame['date'].map(lambda x: re.sub(r" \d{1,2}:\d{2}:\d{2}\+\d{2}:\d{2}", "", str(x)))
    #sentimentDataFrame.to_csv(r"code/SentimentAnalysis/sentiment_df.csv")
    print(sentimentDataFrame)
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

searchHashtagWord = '#Tesla'
numTweetsToPull = 200
df = scrape(searchHashtagWord, numTweetsToPull)
df2 = createdfforapp(df, searchHashtagWord[1:])
print(df2)





