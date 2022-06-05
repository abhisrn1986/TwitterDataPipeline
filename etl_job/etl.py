import time
from collections import deque

import configparser
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
    st.session_state['title'] = st.empty()
    st.session_state['title'].title("Tweets Sentiment Analyser Pipeline")

    # Form to input the tweet query for tweet API Stream filter method.
    form_ph = st.empty()
    form = form_ph.form("Query_form")
    tweets_streaming_query = form.text_input('Tweets Stream Query', 'China')
    query_submitted = form.form_submit_button("Submit", on_click=is_query_sent)

    # Check box to post in a particular slack channel and form for inputting
    # the web hook url.
    enable_slack_post = st.checkbox("Post in slack channel")
    if(enable_slack_post):
        slack_form_widget_ph = st.empty()
        slack_form_widget = slack_form_widget_ph.container()
        slack_web_hook_url = slack_form_widget.text_input(
            "Slack channel web hook url", "Enter the url")
        slack_invalid_text = slack_form_widget.empty()

    tweet_post_widgets = []
    # Deque is used instead of list due better performance of rotation
    # functionality.
    tweet_texts = deque()

    # Check if the tweet query is submitted.
    if "query_submitted" in st.session_state.to_dict() and st.session_state[
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

        # Post to slack whenever there is a change in the mongo db
        # (here the assumption is that the changes are only insertions)
        with db.tweets.watch() as stream:
            for change in stream:
                # st.write("Enterin watch for loop")
                clear_indx = 0

                tweet_dict = change['fullDocument']
                tweet_text = get_tweet_text(tweet_dict)
                score = get_score_tweet(tweet_text)

                # If enable post checkbox is checked than post the tweet
                # sentiment in the given slack channel.
                if(enable_slack_post):
                    if not slack.post_slack(
                            tweet_text, score, get_tweet_image_url(tweet_dict),
                            slack_web_hook_url):
                        slack_invalid_text.markdown(
                            """<p style="color:red"> The slack web url is invalid! Enter a valid one </p>""",
                            unsafe_allow_html=True)

                sentiment_html = utils.get_sentiment_html(
                    get_tweet_sentiment(score))
                html_text = f"""<div style="margin-bottom: 30px"><span style="word-wrap:break-word;">{tweet_text}\n{sentiment_html}</span><div>"""

                # Add tweet sentiments text widgets until the number of these
                # widgets reaches max_tweets_display.
                if len(tweet_post_widgets) < max_tweets_display:
                    tweet_post_widgets.append(st.markdown(
                        html_text, unsafe_allow_html=True))
                    tweet_texts.append(html_text)
                tweet_post_widgets[0].markdown(
                    html_text, unsafe_allow_html=True)

                # When the number of tweets displayed exceeds
                # max_tweets_display than shift content of the markdown
                # widgets by one downwards and add new one at the top.
                for i_text, text in enumerate(tweet_texts):
                    if i_text < len(tweet_texts) - 1:
                        tweet_post_widgets[i_text + 1].markdown(
                            text, unsafe_allow_html=True)
                tweet_texts.rotate(1)
                tweet_texts[0] = html_text

                time.sleep(5)
