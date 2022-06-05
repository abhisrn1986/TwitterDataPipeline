import time
import requests
import credentials


def post_slack(text, score, image_url, web_hook_url):
    """Posts the text and sentimental score along with thumbnail image

    Args:
        text (string): Tweet text to post.
        score (dict): Score from VaderSentimentAnalysis.
        image_url (string): Url of the image for thumbnail
    """

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

    try:
        requests.post(url=web_hook_url, json=data)
        time.sleep(5)
        return True
    except:
        return False
