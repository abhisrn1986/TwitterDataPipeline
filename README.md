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

[<img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" />](https://www.docker.com) 
[<img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" />](https://www.mongodb.com)
[<img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" />](https://www.twitter.com)
[<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />](https://www.python.org)
[<img src="https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white" />](https://www.gnu.org/software/bash)
[<img src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white" />](https://code.visualstudio.com)
[<img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" />](https://pandas.pydata.org)
[<img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" />](https://numpy.org)
[<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" />](https://api.slack.com/bot-users)





## How to Run Locally
