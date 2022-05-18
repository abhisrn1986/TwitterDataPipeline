from tweepy import Stream
import credentials
import pymongo
import json
import time
import os


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


def is_replica_set(mongo_db):
    """Checks if mongoDB client is a replica set.

    Args:
        mongo_db (pymongo.MongoClient): MongoDB client comprising
        of database "tweets".

    Returns:
        bool: True if a replicaset else false.
    """
    try:
        mongo_db.admin.command("replSetGetStatus")
        return True
    except pymongo.errors.OperationFailure:
        return False


if __name__ == '__main__':

    # wait until mongo db is connected properly before insertion
    time.sleep(10)

    # Initialize a mongodb replica set and config it to have only one
    # primary node. Replica set allows to notify db change events such
    # as tweet insertion for instance.
    # https://pymongo.readthedocs.io/en/stable/examples/high_availability.html?highlight=replica#id1
    mongodb_client = pymongo.MongoClient(host="mongodb",
                                         port=27017,
                                         directConnection=True)
    # Check if db is replica set if not initialize it and config it.
    if not is_replica_set(mongodb_client):
        config = {'_id': 'dbrs',
                  'members': [
                      {'_id': 0, 'host': 'mongodb:27017'}
                  ]}
        mongodb_client.admin.command("replSetInitiate", config)

    # Connect ot twitter data base
    db = mongodb_client.twitter

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
        print("phrases", phrases)
    except AttributeError:
        print("Provide a query argument as none is provided")
        exit(1)

    user_stream.filter(track=phrases, languages=['en'])
