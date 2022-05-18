import sentimental_analysis
import tweets_database
import slack
from preprocess_tweets import get_tweet_text, get_tweet_image_url

if __name__ == '__main__':

    db = tweets_database.connect_to_mongodb()

    # Post to slack whenever there is a change in the mongo db
    # (here changes are only insertions)
    with db.tweets.watch() as stream:
        for change in stream:
            tweet_dict = change['fullDocument']
            tweet_text = get_tweet_text(tweet_dict)
            score = sentimental_analysis.get_score_tweet(tweet_text)
            slack.post_slack(tweet_text, score, get_tweet_image_url(tweet_dict))