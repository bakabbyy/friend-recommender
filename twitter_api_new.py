# import packages and authorize application
from collections import defaultdict
import numpy as np
import json
import tweepy
from twitter_creds import *

# pass credentials to authorize Twitter app
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,
                 parser=tweepy.parsers.JSONParser(),
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)


def user_timeline(user_id):
    """
    Returns ~3000 of the most recent tweets of a specific user's timeline and dumps
    into a JSON file.
    ---
    :param user_id: Unique identifier of the Twitter account to fetch tweets
    :return: JSON file export of tweet contents and metadata
    """

    timeline_list = []
    # make initial request for most recent tweets
    for tweets in  tweepy.Cursor(api.user_timeline, user_id=user_id, count=200).pages():
        timeline_list.extend(tweets)

    # extract fields into a list of dictionaries
    post_attrs = ['id', 'created_at', 'in_reply_to_status_id', 'in_reply_to_screen_name', 'in_reply_to_user_id',
                  'favorite_count', 'retweet_count', 'text']

    tweets_dict = [{'id': tweet['id'], 'created_at': tweet['created_at'],
                    'screen_name': tweet['user']['screen_name'], 'user_id': tweet['user']['id'],
                    'in_reply_to_status_id': tweet['in_reply_to_status_id'],
                    'in_reply_to_screen_name': tweet['in_reply_to_screen_name'],
                    'in_reply_to_user_id': tweet['in_reply_to_user_id'],
                    'favorite_count': tweet['favorite_count'], 'retweet_count': tweet['retweet_count'],
                    'text': tweet['text']} for tweet in timeline_tweets]

    return tweets_dict
