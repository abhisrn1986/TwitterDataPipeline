# Twitter Data Pipeline

## Overview
The project comprises a real-time tweets data pipeline, a tweets sentiment analyzer module, and a Slack bot to post the tweets' sentiments. The project uses `SentimentIntensityAnalyzer` from the **VaderSentiment** library. The analyzer gives positive, negative, and compound scores for small texts (such as tweets in this case).

The real-time data pipeline flow is as follows:
  1. Tweets are collected and stored in a database.
  2. The sentiment of the tweets is analyzed.
  3. The tweet sentiment is posted on a Slack channel using a Slack bot.
 
Docker container collects tweets in real-time based on a particular query using the streaming functionality in **Tweepy API**. This docker container stores the tweets in **MongoDB**. As soon as the program inserts new tweets in the database, it sends these tweets to another docker container. This docker container performs a sentimental analysis of the tweets and posts the results in a slack channel using the Slack bot. The tweets collection and storage are independent of the sentimental analysis and Slack posting. 

## Features
1. Streams tweets based on search queries using the Tweepy API.
2. Stores tweets dictionary in a MongoDB database.
3. Tweets' insertion in the tweets storage database is detected using MongoDB replica sets, which provide real-time sentiment analysis and posting of tweets in slack.
4. Two docker containers keep tweets collection and storage independent of the tweet's sentiment analysis and slack posting job.
5. Tweets' sentiments are analyzed using the Vader sentiment analysis.
6. Sentiments of the tweets' are posted in a Slack channel using a Slack bot.
7. Multiple Docker containers are defined and run using Docker compose tool.


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
1. git clone https://github.com/abhisrn1986/TwitterDataPipeline.git.
2. Install docker from instructions [here](https://docs.docker.com/engine/install/ubuntu/).
3. If you don’t want to preface the docker command with sudo, follow the instructions [here](https://docs.docker.com/engine/install/linux-postinstall/).
4. Install docker compose executing the command `sudo apt install docker-compose` in shell.
5. Sign up for a twitter developer account with elevated access (maximum limit of 2 million tweet pulls per month) if you don't have one. Elevated access is mandatory to run this project (as Tweepy API Stream functionality is accessible with elevated access account). Here is a [link]( https://developer.twitter.com/en/docs/platform-overview) on how to get started with Twitter API.
6. Create slackbot to post tweets in a slack channel see the section below on how to do this. 	
7. Create a .env file in root directory (TwitterDataPipeline) consisting of the credentials of twitter and slack channel web hook in the folowing format:

    ```
    CUSTOMER_KEY=key1
    CUSTOMER_SECRET_KEY=key2
    ACCESS_TOKEN=token1
    ACCESS_TOKEN_SECRET=token2
    BEARER_TOKEN=token3
    SLACK_WEBHOOK=url
    ```

    *Note*: Replace the text after = in each line with approriate values (such the customer keys, access tokens, slack webhook url and the query) and remember there shoudn't be any space after =.

8. Build all the docker containers by running `docker-compose build` in terminal within the directory TwitterDataPipeline.
9. To run the pipeline execute bash script run_pipeline.sh as `run_pipeline.sh -q "query1;query2"`. `-q` option is mandatory to provide queries. User can provide as many queries as possible with queries sperated by `;`. For instance, to stream all tweets related with china and germany one can run the command `run_pipeline.sh -q "china;germany"` and if everyhting is configured properly this should post tweets with sentiment score in the slack channel used.

## How to build a slack bot

1. Login and go to Your Apps
2. Choose Create New App
3.Choose the option From scratch
4. Fill in a name and choose your slack workspace as Development Slack Workspace
5. Press Create App
6. Under Add features and functionality click on Incoming Webhooks
7. Activate incoming webhooks by clicking on the switch
8. Click on Add new webhook to the workspace at the bottom of the page
9. Select a channel where you want to post messages and click on Allow
10. Scroll down and copy the Webohook URL into the code.

*Note*: More info can be found [here](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack)
