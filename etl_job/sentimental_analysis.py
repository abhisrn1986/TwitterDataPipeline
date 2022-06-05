from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_score_tweet(tweet_text):
    """Get VaderSentiment score of the tweet text

    Args:
        tweet_text (str): Text for performing sentimental analysis

    Returns:
        dict: Score in the form 
        {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
        refer https://github.com/cjhutto/vaderSentiment
    """

    return get_score_tweet.analyzer.polarity_scores(tweet_text)


def get_tweet_sentiment(score):

    if score['compound'] <= -0.05:
        return 'negative'
    elif score['compound'] >= 0.05:
        return 'positive'
    
    return 'neutral'


get_score_tweet.analyzer = SentimentIntensityAnalyzer()
