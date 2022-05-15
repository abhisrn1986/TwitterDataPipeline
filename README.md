# Twitter Data Pipeline

## Overview
The project comprises a real-time tweets data pipeline, a tweets sentiment analyzer module, and a Slack bot to post the tweets' sentiments. The project uses `SentimentIntensityAnalyzer` from the **VaderSentiment** library. The analyzer gives positive, negative, and compound scores for small texts (such as tweets in this case).

The real-time data pipeline flow is as follows:
  1. Tweets are collected and stored in a database.
  2. The sentiment of the tweets is analyzed.
  3. The tweet sentiment is posted on a Slack channel using a Slack bot.
 
Docker container collects tweets in real-time based on a particular query using the streaming functionality in **Tweepy API**. This docker container stores the tweets in **MongoDB**. As soon as the program inserts new tweets in the database, it sends these tweets to another docker container. This docker container performs a sentimental analysis of the tweets and posts the results in a slack channel using the Slack bot. The tweets collection and storage are independent of the sentimental analysis and Slack posting. 

## Features

## Technology Stack

## How to Run Locally
