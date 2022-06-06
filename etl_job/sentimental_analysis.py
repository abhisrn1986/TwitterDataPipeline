from enum import Enum

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Sentiment(Enum):
    """Enum Type for sentiment of tweets.
    """
    NEUTRAL = 0,
    POSITIVE = 1,
    NEGATIVE = -1

    def __str__(self):
        return f'{self.name}'


def get_score_tweet(tweet_text):
    """Get VaderSentiment score of the tweet text.

    Args:
        tweet_text (str): Text for performing sentimental analysis.

    Returns:
        dict: Score in the form 
        {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
        refer https://github.com/cjhutto/vaderSentiment.
    """

    return get_score_tweet.analyzer.polarity_scores(tweet_text)


def get_tweet_sentiment(score):
    """Get the general sentiment from the sentiment score.

    Args:
        score (float): score from VaderSentimentAnalysis.

    Returns:
        Sentiment: General sentiment.
    """

    if score['compound'] <= -0.05:
        return Sentiment.NEGATIVE
    elif score['compound'] >= 0.05:
        return Sentiment.POSITIVE

    return Sentiment.NEUTRAL


get_score_tweet.analyzer = SentimentIntensityAnalyzer()
