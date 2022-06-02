import time
import os

import json

from tweepy import Stream
import pymongo
import credentials


class UserTweetsStream(Stream):
    """Derived class of Stream class from Twitter API overriding
       on_data method to insert the tweet in a MongoDB database

    Args:
        Stream (Stream): Stream class from twitter API
    """

    def __init__(self, *args, mongo_db, **kargs):
        """Constructor

        Args:
            mongo_db (pymongo.MongoClient): MongoDB client comprising
            of database "tweets".
        """
        self.__db = mongo_db
        super().__init__(*args, **kargs)

    # Insert the new tweets into the mongo db
    def on_data(self, raw_data):
        """On recieving a tweet from the the stream the tweet is
           is inserted in the tweets database of the MongoDB client.

        Args:
            raw_data (dict): Raw data from the twitter stream.
        """
        tweet_data = json.loads(raw_data)
        if self.__db is not None:
            self.__db.tweets.insert_one(dict(tweet_data))

    __db = None


if __name__ == '__main__':

    # Establish a connection to the MongoDB server and connect to twitter database
    db = pymongo.MongoClient(host="mongodb", port=27017,
                             replicaset='dbrs').twitter

    # set up a tweets stream object which directly inserts tweets into
    # the database whenever new tweets are streamed.
    creds = credentials.get_twitter_creds()
    user_stream = UserTweetsStream(creds['customer_key'],
                                   creds['customer_secret_key'],
                                   creds['access_token'],
                                   creds['access_token_secret'],
                                   mongo_db=db)

    try:
        phrases = [i for i in os.getenv("QUERY").split(";")]
    except AttributeError:
        print("Provide a query argument as none is provided")
        exit(1)

    user_stream.filter(track=phrases, languages=['en'])
