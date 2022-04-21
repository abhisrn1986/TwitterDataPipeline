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

    # Insert the new tweets into the mongo db
    def on_data(self, raw_data):
        tweet_data = json.loads(raw_data)
        if self.__db is not None :
            self.__db.tweets.insert_one(dict(tweet_data))
            # print(dict(tweet_data))
        
    __db = None


if __name__ == '__main__':

    # wait until mongo db is connected properly before insertion
    time.sleep(10)
    # mongo db should be set to a replica set from standalone before this
    # before using replicaset in mongod console use rs.initiate() to
    # intiate the replica set
    # https://pymongo.readthedocs.io/en/stable/examples/high_availability.html?highlight=replica#id1
    mongodb_client = pymongo.MongoClient(host="mongodb", port=27017, replicaset='dbrs', directConnection=True)
    db = mongodb_client.twitter

    user_stream = UserTweetsStream(credentials.customer_key, credentials.customer_secret_key,
                                credentials.access_token, credentials.access_token_secret, mongo_db=db)

    try :
        phrases = [i for i in os.getenv("QUERY").split(";")] 
        print("phrases", phrases)
    except AttributeError:
        print("Provide a query argument as none is provided")
        exit(1)

    user_stream.filter(track=phrases, languages=['en'])