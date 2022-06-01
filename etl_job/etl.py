import time
from collections import deque
import copy
import pymongo
import streamlit as st

import sentimental_analysis
import slack
from preprocess_tweets import get_tweet_image_url, get_tweet_text

if __name__ == '__main__':

    # Establish a connection to the MongoDB server and connect to twitter database
    db = pymongo.MongoClient(host="mongodb", port=27017,
                             replicaset='dbrs').twitter

    tweet_posts = []
    tweet_post_text = deque()
    st.title("Tweets Sentiment Analyser Pipeline")
    enable_slack_post = st.checkbox("Post in slack channel")

    # Post to slack whenever there is a change in the mongo db
    # (here changes are only insertions)
    with db.tweets.watch() as stream:
        clear_indx = 0
        for change in stream:
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
