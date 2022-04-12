import pandas as pd
import tweepy
import datetime 

import os
from dotenv import load_dotenv
load_dotenv()

CONSUMER_API_KEY = os.getenv('CONSUMER_API_KEY')
CONSUMER_API_SECRET_KEY = os.getenv('CONSUMER_API_SECRET_KEY')
ACCESS_API_KEY = os.getenv('ACCESS_API_KEY')
ACCESS_API_SECRET_KEY= os.getenv('ACCESS_API_SECRET_KEY')

auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET_KEY)
auth.set_access_token(ACCESS_API_KEY, ACCESS_API_SECRET_KEY)
api = tweepy.API(auth)

def cleanseDate(dataFrame, dateTill):

    joinedTable = pd.DataFrame()
    return joinedTable


def twitterScraper(searchHashtagWord, numTweetsToPull, dateFrom, dateTill):
    isValidDate = checkDateOrder(dateFrom, dateTill)
   
    if (isValidDate == False):
        return
    
    tweet_df = pd.DataFrame(columns=['username', 'description', 'location', 'following', 'followers',  'totaltweets',  'retweetcount', 'text', 'date','hashtags'])

    tweets = tweepy.Cursor(
        api.search_tweets, 
        searchHashtagWord, 
        lang="en",
        since_id=dateFrom,
        tweet_mode='extended').items(numTweetsToPull)
    
    list_tweets = [tweet for tweet in tweets] 
    
    i = 1
 
    # we will iterate over each tweet in the
    # list for extracting information about each tweet
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        date = tweet.created_at
        hashtags = tweet.entities['hashtags']
        
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])
        
        ith_tweet = [username, description,
                             location, following,
                             followers, totaltweets,
                             retweetcount, text, date,hashtext]
                             
        tweet_df.loc[len(tweet_df)] = ith_tweet

    return tweet_df
    
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
numTweetsToPull = 10

dateFrom = "2022-02-23"
dateTill = "2022-03-24"

twitter_df= twitterScraper(searchHashtagWord, numTweetsToPull, dateFrom, dateTill)
filename = 'tweets.csv'

twitter_df.to_csv(filename)














