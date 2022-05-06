import pandas as pd
import tweepy
import datetime 
import os
from dotenv import load_dotenv
load_dotenv()

from cleanseTweets import *
from scrapeTweets import *
from sentimentAnalyze import *

searchHashtagWord = '#Tesla'
numTweetsToPull = 200

#Scrape the tweets using the provided hashtag
#twitter_df= twitterScraper(searchHashtagWord, numTweetsToPull, dateFrom)

#For Testing Purpose(Save physical df locally)
#filename = 'raw_tweets.csv'
#twitter_df.to_csv(filename)

#For Testing Purpose(Read from local df)
#rawDataFrame = pd.read_csv("test_tweet.csv")
rawDataFrame = pd.read_csv("raw_tweets.csv")

#Cleanse Tweets
cleansedDataFrame = cleanseTweets(rawDataFrame)
#cleansedDataFrame.to_csv("cleansed_df.csv")

#Run Sentiment Analysis on the Tweets
sentimentDataFrame = sentimentAnalyze(cleansedDataFrame) 
sentimentDataFrame.to_csv("sentiment_df.csv")
print(sentimentDataFrame)













