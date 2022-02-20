import time

import pandas as pd
import pymongo
from sqlalchemy import create_engine
import numpy as np
import sentimental_analysis
import json
import credentials
import requests
import urllib
import slack


def insert_tweet_in_postgre_db(tweets):
    # Establish a connection with the postgres and
    postgres_password = urllib.parse.quote_plus(postgres_password)

    pg = create_engine(
        f'postgresql://{credentials.postgres_user}:{credentials.postgres_password}@postgresdb:5432/{credentials.postgres_db}', echo=True)

    df = pd.DataFrame({'tweet' : [doc['text'] for doc in tweets], 'sentiment' : [doc['sentiment'] for doc in tweets]} )
    df.to_sql('tweets', pg, if_exists='append')


def connect_to_mongodb():
    # Establish a connection to the MongoDB server
    client = pymongo.MongoClient(host="mongodb", port=27017, replicaset='dbrs')

    # Select the database you want to use withing the MongoDB server
    db = client.twitter

    time.sleep(5)

    return db

