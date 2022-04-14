#1. Cleanse Adequate number of words in text (remove the tweet if it has less than 6 words)
#2. Cleanse Foreign words (remove foreign words from the text, if a big part of the text is non-English, remove the tweet)
#3. Cleanse hashtag (convert hashtags to words, Remove hashtags at the end of words)
#4. Cleanse webadresses (remove webaddresses from the text)
#5. Cleanse Dollarsign(stock ticker symbols)
#6. Cleanse @
#7. Cleanse Emojis

def cleanseTweets(rawDataFrame):
    cleansedDataFrame = rawDataFrame
    return cleansedDataFrame