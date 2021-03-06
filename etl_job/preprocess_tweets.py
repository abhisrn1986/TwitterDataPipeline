import re

def clean_tweet(tweet_text):
    """Removes the hastags, urls, mentions and rts from tweet text.

    Args:
        tweet_text (str): Tweet text to clean.

    Returns:
        str: Cleaned text removing hastags, urls, mentions
             and rts.
    """

    tweet_text = re.sub(clean_tweet.mentions_regex, '', tweet_text)  # removes @mentions
    # removes hashtag symbol
    tweet_text = re.sub(clean_tweet.hashtag_regex, '', tweet_text)
    # removes RT to announce retweet
    tweet_text = re.sub(clean_tweet.rt_regex, '', tweet_text)
    tweet_text = re.sub(clean_tweet.url_regex, '', tweet_text)  # removes most URLs

    return tweet_text

# Patterns used for cleaning the text used exclusively in the 
# clean_tweet method above.
clean_tweet.mentions_regex = '@[A-Za-z0-9]+'
clean_tweet.url_regex = 'https?:\/\/\S+'  # this will not catch all possible URLs
clean_tweet.hashtag_regex = '#'
clean_tweet.rt_regex = 'RT\s'

def extended_tweet_exists(tweet):
    return 'extended_tweet' in tweet

def get_tweet_text(tweet):
    """Extract the complete text of the tweet with no hastags, urls,
        mentions and rts.

    Args:
        tweet (dictionary): Twitter API tweet dictionary.

    Returns:
        str: Extracted full text with no hastags, urls,mentions and rts.
    """

    text = "No text"
    if extended_tweet_exists(tweet):
        text = tweet['extended_tweet']['full_text']
    elif 'retweeted_status' in tweet:
        retweet = tweet['retweeted_status']
        if extended_tweet_exists(retweet):
            text = retweet['extended_tweet']['full_text']
        else:
            text = retweet['text']
    else:
        text = tweet['text']
    
    return clean_tweet(text)

def get_tweet_image_url(tweet):
    """Extract the image url of the tweet if it exists otherwise use
        use the defualt image from "https://about.twitter.com/content/dam/about-twitter/en/brand-toolkit/brand-download-img-1.jpg.twimg.1920.jpg".

    Args:
        tweet (dict): Twitter API tweet dictionary.

    Returns:
        str: Extracted image url.
    """

    image_url = "https://about.twitter.com/content/dam/about-twitter/en/brand-toolkit/brand-download-img-1.jpg.twimg.1920.jpg"
    extended_tweet = {}
    tweet_entities = {}

    # Extract the media url if it exists for image link
    # in the data posted for slack
    if 'retweeted_status' in tweet:
        retweet = tweet['retweeted_status']

        if 'quoted_status' in retweet:
            retweet = retweet['quoted_status']
    
        if 'extended_tweet' in retweet:
            retweet = retweet['extended_tweet']
            text = retweet['full_text']

        tweet_entities = retweet['entities']
        if 'media' in tweet_entities:
            image_url = tweet_entities['media'][0]['media_url']
        elif 'extended_entities' in retweet:
            image_url = extended_tweet['extended_entities']['media'][0]['media_url']
    else :
        tweet_entities = tweet['entities'] 
        if 'media' in tweet_entities:
            image_url = tweet_entities['media'][0]['media_url']

    return image_url



    