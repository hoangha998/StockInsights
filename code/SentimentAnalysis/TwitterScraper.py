import pandas as pd
import tweepy
import datetime 
import os
from dotenv import load_dotenv
load_dotenv()

from cleanseTweets import *
from scrapeTweets import *
from sentimentAnalyze import *

def scrapeAndCleanse(nameOfStock):#Cleanse repeated tweets and retweets
    searchHashtagWord = '#'+nameOfStock
    print(searchHashtagWord)
    numTweetsToPull = 100
    dateFrom = "2022-01-01"

    #Scrape the tweets using the provided hashtag
    ##twitter_df= twitterScraper(searchHashtagWord, numTweetsToPull, dateFrom)

    #For Testing Purpose(Save physical df locally)
    #twitter_df.to_csv('raw_tweets.csv')

    #For Testing Purpose(Read from local df)
    rawDataFrame = pd.read_csv("test_tweet.csv")
    #rawDataFrame = pd.read_csv("raw_tweets.csv")

    #Cleanse Tweets
    ##cleansedDataFrame = cleanseTweets(twitter_df)
    cleansedDataFrame = cleanseTweets(rawDataFrame)
    #cleansedDataFrame.to_csv("cleansed_df.csv")

    #Run Sentiment Analysis on the Tweets
    sentimentDataFrame = sentimentAnalyze(cleansedDataFrame) 
    return sentimentDataFrame 













