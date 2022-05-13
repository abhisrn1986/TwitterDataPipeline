from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_score_tweet(tweet_text):

    return get_score_tweet.analyzer.polarity_scores(tweet_text)

get_score_tweet.analyzer = SentimentIntensityAnalyzer()

