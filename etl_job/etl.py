import socket
import time
from base64 import decode
from collections import deque

import pymongo
import configparser
import streamlit as st

import slack
from preprocess_tweets import get_tweet_image_url, get_tweet_text
from sentimental_analysis import get_score_tweet, get_tweet_sentiment


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


def send_query_to_tweet_stream(query):
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


# Set a parameter in session state for checking if the query is already
# submitted when there are reruns due to intereaction with other widgets.
# Needed to clear the query submission form in the rerun after submitting
# the query initially.
def is_query_sent():
    
    st.session_state['query_submitted'] = True
    st.session_state['title'].title("Tweets Sentiment Analyser Pipeline")



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


    # Get the config of streamlit app setup
    config = configparser.ConfigParser()
    config.read('config.ini')
    max_tweets_display = int(config['streamlit_app']['max_tweets_display'])


    
    # Setup the streamlit elements for parameter passing
    st.session_state['title'] = st.empty()
    st.session_state['title'].title("Tweets Sentiment Analyser Pipeline")


    form_ph = st.empty()
    form = form_ph.form("Query_form")
    tweets_streaming_query = form.text_input('Tweets Stream Query', 'China')
    query_submitted = form.form_submit_button("Submit", on_click=is_query_sent)

    enable_slack_post = st.checkbox("Post in slack channel")

    if(enable_slack_post):
        slack_form_widget_ph = st.empty()

        slack_form_widget = slack_form_widget_ph.container()
        slack_web_hook_url = slack_form_widget.text_input("Slack channel web hook url", "Enter the url")
        slack_invalid_text = slack_form_widget.empty()

    tweet_post_widgets = []
    tweet_texts = deque()


    # Check if the tweet query is submitted
    if "query_submitted" in st.session_state.to_dict() and st.session_state['query_submitted']:
        send_query_to_tweet_stream(tweets_streaming_query)
        # Clear the form as only one set of queries are allowed at the start
        # TODO this can be removed when Twitter API allows changing the stream
        # at run time.
        form_ph.empty()

        st.session_state['tweet_feed_title'] = st.empty()
        st.session_state['tweet_feed_title'].markdown("""<h2> Real time tweets feed </h2>""", unsafe_allow_html=True)

        # Post to slack whenever there is a change in the mongo db
        # (here changes are only insertions)
        with db.tweets.watch() as stream:
            for change in stream:
                # st.write("Enterin watch for loop")
                clear_indx = 0

                tweet_dict = change['fullDocument']
                tweet_text = get_tweet_text(tweet_dict)
                score = get_score_tweet(tweet_text)
                sentiment =  get_tweet_sentiment(score)
                if(enable_slack_post):
                    if not slack.post_slack(tweet_text, score,
                                     get_tweet_image_url(tweet_dict), slack_web_hook_url):

                        slack_invalid_text.markdown("""<p style="color:red"> The slack web url is invalid! Enter a valid one </p>""", unsafe_allow_html=True)
                            

                if sentiment == 'negative':
                    html_color = 'red'
                elif sentiment == 'positive':
                    html_color = 'green'
                else:
                    html_color = 'yellow'

                    
                sentiment_html = f'<p style="color:{html_color}">{sentiment}</p>' 
                html_text = f"""<div style="margin-bottom: 30px"><span style="word-wrap:break-word;">{tweet_text}\n{sentiment_html}</span><div>"""

                if len(tweet_post_widgets) < max_tweets_display:
                    tweet_post_widgets.append(st.markdown(
                        html_text, unsafe_allow_html=True))
                    tweet_texts.append(html_text)
                tweet_post_widgets[0].markdown(html_text,  unsafe_allow_html=True)
                for i_text, text in enumerate(tweet_texts):
                    if i_text < len(tweet_texts) - 1:
                        tweet_post_widgets[i_text + 1].markdown(text,
                                                         unsafe_allow_html=True)

                tweet_texts.rotate(1)
                tweet_texts[0] = html_text

                time.sleep(5)
