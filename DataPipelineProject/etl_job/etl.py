import time
import urllib.parse

import pandas as pd
import pymongo
from sqlalchemy import create_engine
import numpy as np
import os

postgres_db = os.getenv('POSTGRES_DB')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_user = os.getenv('POSTGRES_USER')


# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database you want to use withing the MongoDB server
db = client.twitter

time.sleep(5)

docs = list(db.tweets.find({}, {'_id': 0, "text": 1}))
# docs = docs.find({},{"text"} )
# for doc in docs:
    # print(doc)

if docs :

    df = pd.DataFrame({'tweet' : [doc['text'] for doc in docs], 'sentiment' : np.full(len(docs), 0, dtype=int)})

    postgres_password = urllib.parse.quote_plus(postgres_password)

    pg = create_engine(f'postgresql://{postgres_user}:{postgres_password}@postgresdb:5432/{postgres_db}', echo=True)

    df.to_sql('tweets', pg, if_exists='replace')

    # pg.execute('''
    #     CREATE TABLE IF NOT EXISTS tweets (
    #     text VARCHAR(500),
    #     sentiment NUMERIC
    # );
    # ''')

