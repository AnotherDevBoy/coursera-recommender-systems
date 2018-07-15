from utils import *

import pandas as pd

items = []
users = set()
ratings = None
predictions = None
top_n_by_user = {}
items_popularity = {}

def generate_top_n_for_all_users(users):
    for user_id in users:
        predictions_for_user = predictions[['Item', user_id]]

        predictions_for_user = predictions_for_user.sort_values(by=[user_id], ascending=False)
        top_n_by_user[user_id] = predictions_for_user


def get_ratings(user_id):
    return ratings[['item', user_id]].dropna()


def get_ratings_for_item(user_id, item_id):
    user_ratings = get_ratings(user_id)

    rating = user_ratings.loc[user_ratings['item'] == int(item_id)]

    if rating.empty:
        return None

    return  rating.iloc[0][user_id]


def get_average_user_rating(user_id):
    user_ratings = get_ratings(user_id)
    user_rating_values = list(user_ratings[user_id])

    average_rating = 0.0

    for rating in user_rating_values:
        average_rating += rating

    return average_rating/float(len(user_rating_values))


def is_item_relevant_for_user(user_id, item_id):
    user_rating = get_ratings_for_item(user_id, item_id)

    if not user_rating:
        return False

    average_user_rating = get_average_user_rating(user_id)

    return user_rating >= average_user_rating


def get_predictions(user_id):
    return predictions[['Item', user_id]].dropna()


def get_top_n(user_id, n):
    return top_n_by_user[user_id].head(n=n)


def get_relevant_items_for_user(user_id):
    user_ratings = get_ratings(user_id)
    average_rating = get_average_user_rating(user_id)
    return user_ratings[user_ratings[user_id] >= average_rating]


def get_item_by_id(item_id):
    items_found = [item for item in items if item['id'] == item_id]

    if items_found:
        return items_found[0]

    return -1


def set_items(items_arg):
    global items
    items = items_arg


def get_items():
    return items


def get_users():
    return users


def set_ratings(ratings_arg):
    global ratings
    global items_popularity
    ratings = ratings_arg

    users_that_rated = list(ratings)[1:]
    for index, rating in ratings.iterrows():
        item = rating['item']
        ratings_for_item = 0
        for user in users_that_rated:
            if not np.isnan(rating[user]):
                ratings_for_item += 1

        popularity = float(ratings_for_item)/float(len(users_that_rated))
        items_popularity[item] = popularity


def is_item_popular(item_id):
    return items_popularity[item_id] >= 0.15


def set_predictions(predictions_arg):
    global predictions
    global users
    predictions = predictions_arg
    users = users | set(predictions.columns[1:])