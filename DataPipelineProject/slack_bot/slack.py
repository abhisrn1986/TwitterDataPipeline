


# pip install pyjokes
import pyjokes
import requests

webhook_url = "https://hooks.slack.com/services/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"

joke = pyjokes.get_joke()

data = {'text': joke}
requests.post(url=webhook_url, json = data)