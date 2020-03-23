import os
import pandas as pd
import numpy as np

from flask import Flask, render_template, request, url_for
# from rest_api import get_friends

path = '/Users/baka_brooks/Documents/metis-projects/PASSION-PROJECT/recommender-app/'
os.chdir(path)

# import the data
dists = pd.read_pickle('model/dists.pkl')
orig_profiles = pd.read_pickle('model/orig_profiles.pkl')
personalities = pd.read_pickle('model/full_prof_for_rec.pkl')

# extract personality columns
personalities = personalities.loc[:, ['Openness', 'Conscientiousness',
                                      'Extraversion', 'Agreeableness',
                                      'Emotional range']]

# Initialize the app
app = Flask(__name__)


# @app.route("/about/", methods=["POST", "GET"])
# def about():
#     return render_template('about.html')
#
#
# @app.route("/contact/", methods=["POST", "GET"])
# def contact():
#     return render_template('contact.html')


@app.route("/")
@app.route("/predict/", methods=["POST", "GET"])
def recommend():
    # WHAT GOES HERE
    return render_template("index.html")


# recommender funcntion
def get_friends(screen_name, num_recs=3):
    """
    Outputs a list of friend recommendations based on cosine similarity of the input screen name.
    ---
    :param screen_name: Screen name of the user with which to get friend recommendations.
    :param num_recs: The number of friend recommendations to return.
    :return: List of similar users.
    """
    screen_name = [sn for sn in [screen_name] if sn in dists.columns]
    screen_sum = dists[screen_name].apply(lambda row: np.sum(row), axis=1)
    screen_sum = screen_sum.sort_values(ascending=False)
    ranked_users = screen_sum.index[screen_sum.index.isin(screen_name) == False]
    ranked_users = ranked_users.tolist()

    return ranked_users[:num_recs]

if __name__ == "__main__":
    app.run(debug=True)
