import pandas as pd
import numpy as np
from pprint import pprint

from flask import Flask, render_template, request, url_for

# import the data
dists = pd.read_pickle('model/dists.pkl')
orig_profiles = pd.read_pickle('model/orig_profiles.pkl')
personalities = pd.read_pickle('model/full_prof_for_rec.pkl')

# extract personality columns
personalities = personalities.loc[:, ['Openness', 'Conscientiousness',
                                      'Extraversion', 'Agreeableness',
                                      'Emotional range']]

app = Flask(__name__)


@app.route("/recommend/", methods=["POST", "GET"])
def get_friends(screen_name, num_recs=3):
    """
    Outputs a list of friend recommendations based on cosine similarity of the input screen name.
    ---
    :param screen_name: Screen name of the user with which to get friend recommendations.
    :param num_recs: The number of friend recommendations to return.
    :return: Pandas dataframe of the data that was pulled from the Twitter API.
    """
    screen_name = [sn for sn in [screen_name] if sn in dists.columns]
    screen_sum = dists[screen_name].apply(lambda row: np.sum(row), axis=1)
    screen_sum = screen_sum.sort_values(ascending=False)
    ranked_users = screen_sum.index[screen_sum.index.isin(screen_name) == False]
    ranked_users = ranked_users.tolist()

    return ranked_users[:num_recs]


if __name__ == '__main__':
    app.run(port=3000, debug=True)
    # friends = get_friends(screen_name)
    # print(f'Finding friends for: {screen_name}')
    # print('Recommendations')
    # pprint(friends)
