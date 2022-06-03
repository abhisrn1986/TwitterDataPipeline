from base64 import decode
import socket
import time
from collections import deque

import pymongo
import streamlit as st

import sentimental_analysis
import slack
from preprocess_tweets import get_tweet_image_url, get_tweet_text


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

    # The server's hostname or IP address
    HOST = socket.gethostbyname('tweet_collector')
    PORT = 8888        # The port used by the server

    tweet_posts = []
    tweet_post_text = deque()
    st.title("Tweets Sentiment Analyser Pipeline")

    form = st.form("Query_form")
    tweets_streaming_query = form.text_input('Tweets Stream Query', 'China')
    query_submitted = form.form_submit_button("Submit")

    enable_slack_post = st.checkbox("Post in slack channel")

    if query_submitted:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes(tweets_streaming_query, 'utf-8'))
            data = s.recv(1024)

        data_str = data.decode()
        st.write(f"Received {data_str}")
        form.empty()

        time.sleep(5)

        # Post to slack whenever there is a change in the mongo db
        # (here changes are only insertions)
        with db.tweets.watch() as stream:
            for change in stream:
                # st.write("Enterin watch for loop")
                clear_indx = 0

                tweet_dict = change['fullDocument']
                tweet_text = get_tweet_text(tweet_dict)
                score = sentimental_analysis.get_score_tweet(tweet_text)
                if(enable_slack_post):
                    slack.post_slack(tweet_text, score,
                                     get_tweet_image_url(tweet_dict))
                limit_length = 3
                html_text = f""""<span style="word-wrap:break-word;">{tweet_text}: {score}</span>\n\n"""

                if len(tweet_posts) < limit_length:
                    tweet_posts.append(st.markdown(
                        html_text, unsafe_allow_html=True))
                    tweet_post_text.append(html_text)
                tweet_posts[0].markdown(html_text,  unsafe_allow_html=True)
                for i_text, text in enumerate(tweet_post_text):
                    if i_text < len(tweet_post_text) - 1:
                        tweet_posts[i_text + 1].markdown(text,
                                                         unsafe_allow_html=True)

                tweet_post_text.rotate(1)
                tweet_post_text[0] = html_text

                time.sleep(5)
