import pandas as pd
import tweepy
import datetime 
import os
from dotenv import load_dotenv
load_dotenv()

from cleanseTweets import *
from scrapeTweets import *
from sentimentAnalyze import *

def cleanseDate(dataFrame, dateTill):

    joinedTable = pd.DataFrame()
    return joinedTable
    
def checkDateOrder(dateFrom, dateTill):
    dateFromParse = dateFrom.split('-')
    dateFromYear = int (dateFromParse[0]);
    dateFromMonth = int (dateFromParse[1]);
    dateFromDay = int (dateFromParse[2]);
    
    dateTillParse = dateTill.split('-')
    dateTillYear = int (dateTillParse[0]);
    dateTillMonth = int (dateTillParse[1]);
    dateTillDay = int (dateTillParse[2]);
    
    if (dateTillYear > dateFromYear):
        return True
        
    elif (dateTillYear == dateFromYear):
        if (dateTillMonth > dateFromMonth):
            return True
            
        elif (dateTillMonth == dateFromMonth):
            if (dateTillDay > dateFromDay):
                return True
            
            if (dateTillDay == dateFromDay):
                return True
                
    return False
    
    
searchHashtagWord = '#Tesla'
numTweetsToPull = 200

dateFrom = "2022-01-23"
dateTill = "2022-03-24"

#Make sure date range of tweets is valid
isValidDate = checkDateOrder(dateFrom, dateTill)
assert(not isValidDate == False),  "Date order logic error!"

#Scrape the tweets using the provided hashtag
#twitter_df= twitterScraper(searchHashtagWord, numTweetsToPull, dateFrom)

#For Testing Purpose(Save physical df locally)
#filename = 'raw_tweets.csv'
#twitter_df.to_csv(filename)

#For Testing Purpose(Read from local df)
rawDataFrame = pd.read_csv("test_tweet.csv")
#rawDataFrame = pd.read_csv("raw_tweets.csv")

#Cleanse Tweets
cleansedDataFrame = cleanseTweets(rawDataFrame)
#cleansedDataFrame.to_csv("cleansed_df.csv")

#Tokenize Tweets
tokenizedDataFrame = tokenizeTweets(cleansedDataFrame)
tokenizedDataFrame.to_csv("tokenized_df.csv")

#Apply Word2Vec Sentiment Analysis to Tweet Text
print(cleansedDataFrame)













