import os
def get_slack_webhook():
    return os.getenv('SLACK_WEBHOOK')