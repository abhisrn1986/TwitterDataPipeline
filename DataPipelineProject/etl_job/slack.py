import time

def post_slack(text, score, image_url) :

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

    # requests.post(url=credentials.webhook_url, json = data)
    print(data)
    time.sleep(5)
