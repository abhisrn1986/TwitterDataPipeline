# import json
import requests
import credentials
import time

def post_slack(tweet, score) :

    tweet = tweet['fullDocument']
    text = tweet['text']
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

    data = {'blocks': [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{text} \n score:{score}"
            },
            "accessory": {
                "type": "image",
                "image_url": f"{image_url}",
                "alt_text": "alt text for image"
            }
        }]  
    }

    # TODO remove after proper debugging
    # with open('readme.txt', 'a') as f:
    #     tweet.pop('_id', None)
    #     f.write(json.dumps(tweet))
    #     f.write(f'\n extended tweet: {json.dumps(extended_tweet)}\n')
    #     f.write(f'\ntweet_entities: {json.dumps(tweet_entities)}\n')
    #     f.write(f'\n media_url: {image_url} \n')
    #     f.write(json.dumps(data))
    #     f.write("\n------------------------------------------------------\n")

    requests.post(url=credentials.webhook_url, json = data)
    time.sleep(5)
