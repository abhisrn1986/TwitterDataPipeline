import os

def get_twitter_creds():
    
    return { 'customer_key' : os.getenv("CUSTOMER_KEY"),
    'customer_secret_key' : os.getenv("CUSTOMER_SECRET_KEY"),
    'access_token' : os.getenv("ACCESS_TOKEN"),
    'access_token_secret' : os.getenv("ACCESS_TOKEN_SECRET"),
    'bearer_token' : os.getenv("BEARER_TOKEN")}