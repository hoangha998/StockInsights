import pandas as pd
import os
import sys
import nltk

path = os.getcwd()
parentPath = os.path.dirname(path)
pathToNLTK=parentPath+'/SentimentAnalysis'+'/nltk_data'
nltk.data.path.append(pathToNLTK) #Set path of nltk library to current repository
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentimentAnalyze(cleansedTweets_df):

    for index, row in cleansedTweets_df['text'].iteritems():
        score = SentimentIntensityAnalyzer().polarity_scores(row)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
     
        if neg > pos:
            cleansedTweets_df.loc[index, 'sentiment'] = "negative"
        elif pos > neg:
            cleansedTweets_df.loc[index, 'sentiment'] = "positive"
        else:
            cleansedTweets_df.loc[index, 'sentiment'] = "neutral"
            
        cleansedTweets_df.loc[index, 'neg'] = neg
        cleansedTweets_df.loc[index, 'neu'] = neu
        cleansedTweets_df.loc[index, 'pos'] = pos
        cleansedTweets_df.loc[index, 'compound'] = comp
        
    analyzedTweets_df=cleansedTweets_df
    return analyzedTweets_df