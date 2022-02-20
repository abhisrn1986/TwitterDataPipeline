from tweepy import Stream
import credentials
import pymongo
import json
import time
import os

class UserTweetsStream(Stream):

    def __init__(self, *args, mongo_db, **kargs):
        self.__db = mongo_db
        super().__init__(*args, **kargs)

    # insert the new tweets into the mongo db
    def on_data(self, raw_data):
        tweet_data = json.loads(raw_data)
        if self.__db is not None :
            self.__db.tweets.insert_one(dict(tweet_data))

    __db = None



if __name__ == '__main__':
    # mongo db should be set to a replica set from standalone before this
    mongodb_client = pymongo.MongoClient(host="mongodb", port=27017, replicaset='dbrs')
    db = mongodb_client.twitter

    # wait until mongo db is connected properly before insertion
    time.sleep(5)

    user_stream = UserTweetsStream(credentials.customer_key, credentials.customer_secret_key,
                                credentials.access_token, credentials.access_token_secret, mongo_db=db)


    # TODO may convert this into arguements passed while running docker-compose
    user_stream.filter(track=['Germany'], languages=['en'])
    # user_stream.filter(track=['China'], languages=['en'])
    # user_stream.filter(os.getenv("hashtag"), languages=['en'])