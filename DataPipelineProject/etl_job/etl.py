import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import sentimental_analysis
import tweets_database
import slack
import time
from preprocess_tweets import get_tweet_text, get_tweet_image_url

if __name__ == '__main__':
    # wait until mongo db is connected properly and initialized in
    # get_tweet
    time.sleep(20)

    db = tweets_database.connect_to_mongodb()

    # Post to slack whenever there is a change in the 
    # mongo db (here changes are only insertions)
    with db.tweets.watch() as stream:
        for change in stream:
            tweet_text = get_tweet_text(change)
            score = sentimental_analysis.get_score_tweet(tweet_text)
            slack.post_slack(tweet_text, score, get_tweet_image_url(change))


