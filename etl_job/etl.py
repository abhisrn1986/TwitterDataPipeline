import time
from collections import deque

import configparser
from requests import session
import streamlit as st

import slack
from preprocess_tweets import get_tweet_image_url, get_tweet_text
from sentimental_analysis import get_score_tweet, get_tweet_sentiment
import utils


def is_query_sent():
    """ Set a parameter in session state for checking if the query is already
        submitted when there are reruns due to intereaction with other widgets.
        Needed to clear the query submission form in the rerun after submitting
        the query initially.
    """
    st.session_state['query_submitted'] = True

def add_previous_tweets(tweet_post_text_widgets, tweet_post_img_widgets):
    """Create new widgets for tweet feeds from the previous run tweet feed
       texts and images. 

    Args:
        tweet_post_text_widgets (list): list of tweet feed text widgets of
                                        the current run.
        tweet_post_img_widgets (list): list of tweet feed image widgets of
                                       the current run.
    """

    for text in st.session_state['tweet_texts']:
        tweet_post_img_widgets.append(st.image(text[1], width=128))
        tweet_post_text_widgets.append(st.markdown(
        text[0], unsafe_allow_html=True))



if __name__ == '__main__':

    # wait until mongo db is connected properly before insertion
    time.sleep(10)

    # Initialize a mongodb replica set and config it to have only one
    # primary node. Replica set allows to notify db change events such
    # as tweet insertion for instance.
    # https://pymongo.readthedocs.io/en/stable/examples/high_availability.html?highlight=replica#id1
    # and connect ot twitter database.
    db = utils.get_mongodb_replica_set().twitter

    # Get the config of streamlit app setup.
    config = configparser.ConfigParser()
    config.read('config.ini')
    max_tweets_display = int(config['streamlit_app']['max_tweets_display'])

    # Setup the streamlit elements for parameter passing
    st.title("Tweets Sentiment Analyser Pipeline")


    # Form to input the tweet query for tweet API Stream filter method.
    form_ph = st.empty()
    form = form_ph.form("Query_form")
    tweets_streaming_query = form.text_input('Tweets Stream Query', 'China')
    query_submitted = form.form_submit_button("Submit", on_click=is_query_sent)

    # Check box to post in a particular slack channel and form for inputting
    # the web hook url.
    enable_slack_post = st.checkbox("Post in slack channel")
    slack_form_widget_ph = st.empty()

    if(enable_slack_post):
        slack_form_widget = slack_form_widget_ph.container()
        slack_web_hook_url = slack_form_widget.text_input(
            "Slack channel web hook url", "Enter the url")
        slack_invalid_text = slack_form_widget.empty()


    
    # Deque is used instead of list due better performance of rotation
    # functionality. This basically saves the tweets from previous run
    # of the streamlit app so that new widgets with the same tweet text
    # and images can be created to maintian continuity of the feed.
    if 'tweet_texts' not in st.session_state:
        st.session_state['tweet_texts'] = deque()


    # Check if the tweet query is submitted.
    if "query_submitted" in st.session_state and st.session_state[
            'query_submitted']:
        utils.send_query_to_tweet_stream(tweets_streaming_query)
        # Clear the form as only one set of queries are allowed at the start
        # TODO this can be removed when Twitter API allows changing the stream
        # at run time.
        form_ph.empty()

        # Header for tweet sentiments feed and this is stored in session state
        # to not change across streamlit app reruns.
        st.session_state['tweet_feed_title'] = st.empty()
        st.session_state['tweet_feed_title'].markdown(
            """<h2> Real time tweets feed </h2>""", unsafe_allow_html=True)


        tweet_post_text_widgets = []
        tweet_post_img_widgets = []

        add_previous_tweets(tweet_post_text_widgets, tweet_post_img_widgets)

        # Post to slack whenever there is a change in the mongo db
        # (here the assumption is that the changes are only insertions)
        with db.tweets.watch() as stream:
            for change in stream:
                # st.write("Enterin watch for loop")
                clear_indx = 0

                tweet_dict = change['fullDocument']
                tweet_text = get_tweet_text(tweet_dict)
                score = get_score_tweet(tweet_text)
                thumbnail_url = get_tweet_image_url(tweet_dict)
                sentiment = get_tweet_sentiment(score)

                # If enable post checkbox is checked than post the tweet
                # sentiment in the given slack channel.
                if(enable_slack_post):
                    if not slack.post_slack(
                            tweet_text, score, thumbnail_url,
                            slack_web_hook_url):
                        slack_invalid_text.markdown(
                            """<p style="color:red"> The slack web url is invalid! Enter a valid one </p>""",
                            unsafe_allow_html=True)

                
                html_text = utils.get_tweet_sentiment_html(tweet_text, sentiment)

                # Add tweet sentiments text widgets until the number of these
                # widgets reaches max_tweets_display.
            
                if len(st.session_state['tweet_texts']) < max_tweets_display:
                    
                    tweet_post_img_widgets.append(st.image(thumbnail_url, width=128))
                    tweet_post_text_widgets.append(st.markdown(
                        html_text, unsafe_allow_html=True))
                    
                    st.session_state['tweet_texts'].append((html_text, thumbnail_url))

                
                tweet_post_img_widgets[0].image(
                    thumbnail_url, width=128)
                tweet_post_text_widgets[0].markdown(
                    html_text, unsafe_allow_html=True)

                # When the number of tweets displayed exceeds
                # max_tweets_display than shift content of the markdown
                # widgets by one downwards and add new one at the top.
                for i_text, text in enumerate(st.session_state['tweet_texts']):
                    if i_text < len(st.session_state['tweet_texts']) - 1:
                        tweet_post_img_widgets[i_text + 1].image(
                        text[1], width=128)
                        tweet_post_text_widgets[i_text + 1].markdown(
                        text[0], unsafe_allow_html=True)
                st.session_state['tweet_texts'].rotate(1)
                st.session_state['tweet_texts'][0] = (html_text,thumbnail_url)

                time.sleep(5)
