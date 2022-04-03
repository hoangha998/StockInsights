import pandas as pd
import tweepy

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

def twitterScraper(searchHashtagWord, numTweetsToPull, dateSince):
    tweet_df= pd.DataFrame()   
    
    tweets = tweepy.Cursor(api.search_tweets, 
        searchHashtagWord, 
        lang="en",
        since_id=dateSince,
        tweet_mode='extended').items(numTweetsToPull)
    
    
    return tweet_df
    
searchHashtagWord = 'Tesla'
numTweetsToPull = 10
dateSince = "2022-03--22"

twitterScraper(searchHashtagWord, numTweetsToPull, dateSince)