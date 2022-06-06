import socket

import pymongo

from sentimental_analysis import Sentiment


def get_tweet_sentiment_html(tweet_text, sentiment):
    """Get the html text for streamlit markdown to display the tweet general
       sentiment.

    Args:
        sentiment (Sentiment): General sentiment.

    Returns:
        str: html of sentiment red color for Negative, green for Positive and
             yellow for Neutral.
    """
    if sentiment == Sentiment.NEGATIVE:
        html_color = 'red'
    elif sentiment == Sentiment.POSITIVE:
        html_color = 'green'
    else:
        html_color = 'yellow'

    sentiment_html  = f'<p style="color:{html_color}">{sentiment}</p>'

    return f"""<div style="margin-bottom: 50px"><div><span style="word-wrap:break-word;">{tweet_text}</span></div><div>{sentiment_html}</div></div>"""

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

def get_mongodb_replica_set():
    """ Init a mongodb replica set and return the pymongo client.

    Returns:
        pymongo.MongoClient: pymongo client
    """
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

    return mongodb_client


def send_query_to_tweet_stream(query):
    """Pass the query to tweet collector process via python socket
       communication

    Args:
        query (str): query for filterting tweets in Twitter API tweets
                     streaming.

    Returns:
        bool: True when connection and passing of query was successfull.
    """
    # The server's hostname or IP address
    HOST = socket.gethostbyname('tweet_collector')
    PORT = 8888        # The port used by the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes(query, 'utf-8'))
    except ConnectionRefusedError:
        return False
    return True
    