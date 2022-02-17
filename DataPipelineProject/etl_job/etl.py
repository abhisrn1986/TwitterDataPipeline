import time
import urllib.parse

import pandas as pd
import pymongo
from sqlalchemy import create_engine
import numpy as np
import os
import json, re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


postgres_db = os.getenv('POSTGRES_DB')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_user = os.getenv('POSTGRES_USER')

mentions_regex= '@[A-Za-z0-9]+'
url_regex='https?:\/\/\S+' #this will not catch all possible URLs
hashtag_regex= '#'
rt_regex= 'RT\s'

def clean_tweets(tweet):
    tweet = re.sub(mentions_regex, '', tweet)  #removes @mentions
    tweet = re.sub(hashtag_regex, '', tweet) #removes hashtag symbol
    tweet = re.sub(rt_regex, '', tweet) #removes RT to announce retweet
    tweet = re.sub(url_regex, '', tweet) #removes most URLs
    
    return tweet


analyzer = SentimentIntensityAnalyzer()


# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017, replicaset='dbrs')

# Select the database you want to use withing the MongoDB server
db = client.twitter

time.sleep(5)

# docs = list(db.tweets.find({}, {'_id': 0, "text": 1}))
# # docs = docs.find({},{"text"} )
# # for doc in docs:
#     # print(doc)

# if docs :

#     df = pd.DataFrame({'tweet' : [doc['text'] for doc in docs], 'sentiment' : np.full(len(docs), 0, dtype=int)})

#     postgres_password = urllib.parse.quote_plus(postgres_password)

#     pg = create_engine(f'postgresql://{postgres_user}:{postgres_password}@postgresdb:5432/{postgres_db}', echo=True)

#     df.to_sql('tweets', pg, if_exists='append')

#     # pg.execute('''
#     #     CREATE TABLE IF NOT EXISTS tweets (
#     #     text VARCHAR(500),
#     #     sentiment NUMERIC
#     # );
#     # ''')

with db.tweets.watch() as stream:
    with open('readme.txt', 'w') as f:
        for change in stream:
            tweet = change['fullDocument']['text']
            score = analyzer.polarity_scores(clean_tweets(tweet))

            f.write(f"{tweet} : {score['compound']}")
            f.write("\n------------------------------------------------------\n")
