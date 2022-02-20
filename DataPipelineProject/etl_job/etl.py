import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import sentimental_analysis
import tweets_database
import slack

if __name__ == '__main__':

    db = tweets_database.connect_to_mongodb()

    # with open('readme.txt', 'w') as f:
    #     pass

    # Post to slack whenever there is a change in the 
    # mongo db (here changes are only insertions)
    with db.tweets.watch() as stream:
        for change in stream:
            score = sentimental_analysis.get_score_tweet(change['fullDocument']['text'])
            slack.post_slack(change, score)

