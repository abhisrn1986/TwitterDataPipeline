import re

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def clean_tweets(tweet_text):

    tweet_text = re.sub(clean_tweets.mentions_regex, '', tweet_text)  # removes @mentions
    # removes hashtag symbol
    tweet_text = re.sub(clean_tweets.hashtag_regex, '', tweet_text)
    # removes RT to announce retweet
    tweet_text = re.sub(clean_tweets.rt_regex, '', tweet_text)
    tweet_text = re.sub(clean_tweets.url_regex, '', tweet_text)  # removes most URLs

    return tweet_text
# patterns used for cleaning the text used exclusively in the 
# clean_tweet method above
clean_tweets.mentions_regex = '@[A-Za-z0-9]+'
clean_tweets.url_regex = 'https?:\/\/\S+'  # this will not catch all possible URLs
clean_tweets.hashtag_regex = '#'
clean_tweets.rt_regex = 'RT\s'



def get_score_tweet(tweet):

    return get_score_tweet.analyzer.polarity_scores(clean_tweets(tweet))

get_score_tweet.analyzer = SentimentIntensityAnalyzer()

