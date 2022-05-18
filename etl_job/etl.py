import slack
import pymongo
import sentimental_analysis
from preprocess_tweets import get_tweet_text, get_tweet_image_url

if __name__ == '__main__':

    # db = tweets_database.connect_to_mongodb()
    # Establish a connection to the MongoDB server and connect to twitter database
    db = pymongo.MongoClient(host="mongodb", port=27017, replicaset='dbrs').twitter


    # Post to slack whenever there is a change in the mongo db
    # (here changes are only insertions)
    with db.tweets.watch() as stream:
        for change in stream:
            tweet_dict = change['fullDocument']
            tweet_text = get_tweet_text(tweet_dict)
            score = sentimental_analysis.get_score_tweet(tweet_text)
            slack.post_slack(tweet_text, score, get_tweet_image_url(tweet_dict))