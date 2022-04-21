import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import sentimental_analysis
import tweets_database
import slack
import time

if __name__ == '__main__':
    # wait until mongo db is connected properly and initialized in
    # get_tweet
    time.sleep(20)

    db = tweets_database.connect_to_mongodb()

    # Post to slack whenever there is a change in the 
    # mongo db (here changes are only insertions)
    with db.tweets.watch() as stream:
        for change in stream:
            score = sentimental_analysis.get_score_tweet(change['fullDocument']['text'])
            slack.post_slack(change, score)


