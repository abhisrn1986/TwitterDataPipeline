FROM python:3.9
WORKDIR /get_tweet
COPY requirements.txt /get_tweet
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENTRYPOINT [ "python", "get_tweet.py"]
