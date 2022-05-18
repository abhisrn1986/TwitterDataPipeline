import time
import requests
import credentials


def post_slack(text, score, image_url) :
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

    requests.post(url=credentials.get_slack_webhook(), json = data)
    # print(text , score, image_url)
    time.sleep(5)
