import pandas as pd
import tweepy
import datetime 

import os
from dotenv import load_dotenv
load_dotenv()

import re

from wordsegment import load, segment #wordsegment package splits multiword hashtags into individual words.

#1. Cleanse webadresses (remove webaddresses from the text)
#2. Cleanse Dollarsign(stock ticker symbols)
#3. Cleanse Mention (@)
#4. Cleanse Non-English Characters(Emojis, hashtags, foreign language char)
#5. Cleanse Adequate number of words in text (remove the tweet if it has less than 6 words)
#6. Cleanse Time off date


def cleanseRepeatedTweets(input_df):#Cleanse repeated tweets and retweets
    return (input_df.drop_duplicates(subset='text', keep="first"))

def cleanseWebAddresses(inputString):#Removes any video links or hyper links from the tweet text
    return (re.sub('http://\S+|https://\S+', '', inputString))

def cleanseDollarSign(inputString): #Removes company stock ticker ($) from tweet text
    return (re.sub("\$[A-Za-z0-9_]+","", inputString))

def cleanseMention(inputString): #Removes @(username) from the tweet text
    return (re.sub("@[A-Za-z0-9_]+","", inputString))
    
def cleanseNonEnglishChar(inputString): #Removes emoji ASCII, hashtag, and non-English foreign char. Gets string with char between a to z or digits and whitespace characters.
    return(re.sub(r'[^\w\s]', '', inputString))
    
def cleanseLeadingTrailingWhiteSpace(inputString): #Removes different indentation and return new lines in the text  
    return(inputString.strip())

#def cleanseDateTime(inputString): #Removes the time 


def cleanseTweets(raw_df):
    
    raw_df = cleanseRepeatedTweets(raw_df)
    print(raw_df.shape)
    
    for index, row in raw_df.iterrows():
        text = row['text']
        cleansedString = cleanseWebAddresses(text)
        cleansedString = cleanseLeadingTrailingWhiteSpace(cleansedString)
        cleansedString = cleanseDollarSign(cleansedString)
        cleansedString = cleanseMention(cleansedString)
        cleansedString = cleanseNonEnglishChar(cleansedString)
        
        raw_df.at[index,'text'] = cleansedString
        
        print(cleansedString)
        print("line")
    
    
    #cleansed_df.to_csv('cleansed_df.csv')
    print(raw_df)
    return raw_df
    
    
