
import requests

webhook_url = "https://hooks.slack.com/services/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"


def post_slack(tweet) :
    requests.post(url=webhook_url, json = tweet)