# User Personality Recommender
**Motivation**

Social media as a whole is the new face of the modern day ad industry. Everyday, platforms are in a constant battle for consumer attention as their sole focus is to monetize that attention in a cycle dubbed the ["attention economy"](https://www.nngroup.com/articles/attention-economy/). But what remains unseen is the impact that the constant bombardment of content has had on society, especially to young people. In a world that favors the sources that draw the most attention, we've lost what it means to be authentic in favor of flamboyant personas.

The aim for this project is to create healthier digital spaces. I want to promote meaningful interactions and foster real relationships between people. To find connections without the need for a flood of content, but by trying to find a deeper understanding of an individual using other attributes of their digital footprint.

**Factoids**

- A recent [Cigna study](https://www.cnbc.com/2020/01/23/loneliness-is-rising-younger-workers-and-social-media-users-feel-it-most.html) found that 73% of Gen Z (18–22 year olds, notably the first generation to grow up with technology since day one) report “sometimes” or “always” feeling alone, up from 69% the previous year.

- Every second, approximately 6,000 Tweets are tweeted on Twitter, which corresponds to over 350,000 tweets sent per minute, 500 million tweets per day and around 200 billion tweets per year [(via Brandwatch)](https://www.brandwatch.com/blog/twitter-stats-and-statistics/).

- [Pew Research Center](https://www.pewresearch.org/internet/fact-sheet/social-media/) states that currently, 72% of the public uses some type of social media.

**Problem Statement** 

In this project, I've used three Twitter data sources to create a feature set by utilizing NLP to derive personality classifications via KMeans segmentation. These features were used as the basis for a recommendation engine to connect Twitter users. 

The recommender algorithm does not use original content, that being Tweets that each user has posted to their own account. Derivation of user personalities, sentiment analysis, and ultimately segmentation of Twitter users, are created based upon Tweets that a user has favorited, retweeted, and the attributes of the account and first degree connections.

## Description of the Data

All data is extracted from the Twitter API via the tweepy package. 

### user_timeline

| Independent Variable    | Type            | Description                                                  |
| ----------------------- | --------------- | ------------------------------------------------------------ |
| id                      | Int             | Unique identifier of the tweet.                              |
| created_at              | Timestamp       | Time the tweet was posted.                                   |
| screen_name             | String (Object) | Username of the account that posted the tweet.               |
| user_id                 | Int             | Unique identifier of the account.                            |
| in_reply_to_status_id   | Int             | Unique identifier of the parent tweet to which the tweet is in response to. |
| in_reply_to_screen_name | String (Object) | Username of the account of the parent tweet to which the tweet is in response to. |
| in_reply_to_user_id     | Int             | Unique identifier of the account of the parent tweet to which the tweet is in response to. |
| favorite_count          | Int             | Number of favorites the tweet has.                           |
| retweet_count           | Int             | Number of retweets the tweets has.                           |
| text                    | String (Object) | The text of the tweet.                                       |

### user_favorites

| Independent Variable | Type            | Description                                    |
| -------------------- | --------------- | ---------------------------------------------- |
| id                   | Int             | Unique identifier of the tweet.                |
| created_at           | Timestamp       | Time the tweet was posted.                     |
| screen_name          | String (Object) | Username of the account that posted the tweet. |
| user_id              | Int             | Unique identifier of the account.              |
| favorite_count       | Int             | Number of favorites the tweet has.             |
| retweet_count        | Int             | Number of retweets the tweets has.             |
| text                 | String (Object) | The text of the tweet.                         |

### user_attributes

| Independent Variable | Type            | Description                                                  |
| -------------------- | --------------- | ------------------------------------------------------------ |
| user_id              | Int             | Unique identifier of the account.                            |
| screen_name          | String (Object) | Username of the account.                                     |
| followers_count      | Int             | The number of followers the user has.                        |
| friends_count        | Int             | The number of accounts the user follows.                     |
| favorites_count      | Int             | The number of tweets the user has favorited.                 |
| statuses_count       | Int             | The number of statuses the user has favorited.               |
| following_ids        | Int, List       | List of IDs corrseponding to the accounts the user follows.  |
| follower_ids         | Int, List       | List of IDs corresponding to the accounts that follow the parent user. |

## Files

[get_twitter_data.py](https://github.com/bakabrooks/friend-recommender/blob/master/get_twitter_data.py) contains the script to pull all three data sources from the Twitter API. The script exports the three data sources (user_timeline, user_favorites, and user_attributes) into separate JSON files.



[cleaning.ipynb](https://github.com/bakabrooks/friend-recommender/blob/master/cleaning.ipynb) shows the process of training various supervised learning models, tuning the models and evaluating their effectiveness.



The slide deck for this project can be found [here](https://github.com/bakabrooks/twitter-nlp-sentiment/blob/master/project-04-slides.pdf).