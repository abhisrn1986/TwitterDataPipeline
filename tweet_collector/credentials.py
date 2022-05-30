import os


def get_twitter_creds():
    """Returns the dict with all the credentials of Twitter developer
       account.

    Returns:
        dict: Credentials dict with keys
              customer_key, customer_secret_key, access_token_secret,
              bearer_token.
    """

    return {'customer_key': os.getenv("CUSTOMER_KEY"),
            'customer_secret_key': os.getenv("CUSTOMER_SECRET_KEY"),
            'access_token': os.getenv("ACCESS_TOKEN"),
            'access_token_secret': os.getenv("ACCESS_TOKEN_SECRET"),
            'bearer_token': os.getenv("BEARER_TOKEN")}
