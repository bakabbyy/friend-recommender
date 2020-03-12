# import packages and authorize application
import json
import tweepy
from twitter_creds import *

# pass credentials to authorize Twitter app
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def user_timeline(user_id):
    """
    Returns ~3000 of the most recent tweets of a specific user's timeline and dumps
    into a JSON file.
    ---
    :param user_id: Unique identifier of the Twitter account to fetch tweets
    :return: JSON file export of tweet contents and metadata
    """
    timeline_tweets = []

    try:
        # make initial request for most recent tweets
        timeline = api.user_timeline(user_id=user_id, count=200)

        # save most recent tweets
        timeline_tweets.extend(timeline)

        # save the id of the oldest tweet less one
        oldest = timeline_tweets[-1]['id'] - 1

        # continue where from the last id until there are no tweets left to collect
        while len(timeline) > 0:
            print(f'getting tweets before {oldest}s')

            # all subsequent requests use the max_id param to prevent duplicates
            timeline = api.user_timeline(user_id=user_id, count=200, max_id=oldest)

            timeline_tweets.extend(timeline)

            oldest = timeline_tweets[-1]['id'] - 1

            print(f'...{len(timeline_tweets)}s tweets downloaded so far')

    except IndexError:
        pass

    # extract fields into a list of dictionaries
    tweets_dict = [{'id': tweet['id'], 'created_at': tweet['created_at'],
                    'screen_name': tweet['user']['screen_name'], 'user_id': tweet['user']['id'],
                    'in_reply_to_status_id': tweet['in_reply_to_status_id'],
                    'in_reply_to_screen_name': tweet['in_reply_to_screen_name'],
                    'in_reply_to_user_id': tweet['in_reply_to_user_id'],
                    'favorite_count': tweet['favorite_count'], 'retweet_count': tweet['retweet_count'],
                    'text': tweet['text']} for tweet in timeline_tweets]

    return tweets_dict


def user_favorites(user_id):
    """
    Returns ~3000 of the most recent tweets that a specific user has favorited
    and dumps into a JSON file.
    ---
    :param user_id: Unique identifier of the Twitter account to fetch tweets
    :return: JSON file export of tweet contents and metadata
    """
    favorite_tweets = []

    try:
        # make initial request for most recent tweets
        favorites = api.favorites(user_id=user_id, count=200)

        # save most recent tweets
        favorite_tweets.extend(favorites)

        # save the id of the oldest tweet less one
        oldest = favorite_tweets[-1]['id'] - 1

        # continue where from the last id until there are no tweets left to collect
        while len(favorites) > 0:
            print(f'getting tweets before {oldest}s')

            # all subsequent requests use the max_id param to prevent duplicates
            favorites = api.favorites(user_id=user_id, count=200, max_id=oldest)

            favorite_tweets.extend(favorites)

            oldest = favorite_tweets[-1]['id'] - 1

            print(f'...{len(favorite_tweets)}s tweets downloaded so far')

    except IndexError:
        pass

    # extract fields into a list of dictionaries
    favorites_dict = [{'favorited_by_id': user_id, 'id': tweet['id'],
                       'created_at': tweet['created_at'],
                       'screen_name': tweet['user']['screen_name'],
                       'user_id': tweet['user']['id'],
                       'in_reply_to_status_id': tweet['in_reply_to_status_id'],
                       'in_reply_to_screen_name': tweet['in_reply_to_screen_name'],
                       'in_reply_to_user_id': tweet['in_reply_to_user_id'],
                       'favorite_count': tweet['favorite_count'],
                       'retweet_count': tweet['retweet_count'],
                       'text': tweet['text']} for tweet in favorite_tweets]

    return favorites_dict


def user_profile(user_id):
    """
    Returns the profile information and friends/followers lists of a specific user.
    ---
    :param user_id: Unique identifier of the Twitter account to information
    :return: JSON file export of tweet contents and metadata
    """
    # get user profile information
    info = api.get_user(user_id=user_id)

    # extract fields into a dictionary
    profile_dict = {'user_id': info['id'], 'screen_name': info['screen_name'],
                    'followers_count': info['followers_count'],
                    'friends_count': info['friends_count'],
                    'favourites_count': info['favourites_count'],
                    'statuses_count': info['statuses_count']}

    # use cursor to page through all friends and create list of friend ids
    all_friends = []
    for friend in tweepy.Cursor(api.friends_ids, user_id=user_id, count=200).pages():
        all_friends.extend(friend['ids'])

    # use cursor to page through all followers and create list of follower ids
    all_followers = []
    for follower in tweepy.Cursor(api.followers_ids, user_id=user_id, count=200).pages():
        all_followers.extend(follower['ids'])

    # add lists of friends and followers ids to user_info dictionary
    profile_dict['follower_ids'] = all_followers
    profile_dict['friend_ids'] = all_friends

    return profile_dict


# initialize empty containers with host account's info
timelines = [user_timeline(2649540547)]
favorites = [user_favorites(2649540547)]
profiles = [user_profile(2649540547)]

# extract follower ids list from my twitter account
my_followers = profiles[0]['follower_ids']



#################### CREATE FUNCTION TO SIMPLIFY THE BELOW ####################



# loop through follower ids and add list of timeline tweets for each user
for idx, user_id in enumerate(my_followers):
    try:
        timelines.append(user_timeline(user_id))
        print('Appended {} of {} timelines...'.format(idx+1, len(my_followers)))
    except tweepy.TweepError:
        print("Failed to run the command on that user, Skipping...")

with open(f'timelines_{stop}.json', 'w') as fout:
    json.dump(timelines, fout)

# loop through follower ids and add list of favorite tweets for each user
for idx, user_id in enumerate(my_followers):
    try:
        favorites.append(user_favorites(user_id))
        print('Appended {} of {} timelines...'.format(idx+1, len(my_followers)))
    except tweepy.TweepError:
        print("Failed to run the command on that user, Skipping...")

with open(f'favorites_{stop}.json', 'w') as fout:
    json.dump(favorites, fout)

# loop through follower ids and add list of profiles
for idx, user_id in enumerate(my_followers):
    try:
        profiles.append(user_profile(user_id))
        print('Appended {} of {} timelines...'.format(idx+1, len(my_followers)))
    except tweepy.TweepError:
        print("Failed to run the command on that user, Skipping...")

with open(f'profiles._{stop}json', 'w') as fout:
    json.dump(profiles, fout)