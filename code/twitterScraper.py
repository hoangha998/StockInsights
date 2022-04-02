import pandas as pd
import tweepy

import os
from dotenv import load_dotenv
load_dotenv()

CONSUMER_API_KEY = os.getenv('CONSUMER_API_KEY')
CONSUMER_API_SECRET_KEY = os.getenv('CONSUMER_API_SECRET_KEY')
ACCESS_API_KEY = os.getenv('ACCESS_API_KEY')
ACCESS_API_SECRET_KEY= os.getenv('ACCESS_API_SECRET_KEY')

print("Consumer API Key = " + CONSUMER_API_KEY)
print("Consumer API Secret Key = " + CONSUMER_API_SECRET_KEY)
print("Access API Key = " + ACCESS_API_KEY)
print("Access API Secret Key = " + ACCESS_API_SECRET_KEY)

auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET_KEY)
auth.set_access_token(ACCESS_API_KEY, ACCESS_API_SECRET_KEY)
api = tweepy.API(auth)

