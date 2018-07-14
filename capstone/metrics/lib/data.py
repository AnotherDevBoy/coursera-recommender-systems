from utils import *

import pandas as pd

items = []
users = set()
ratings = None
predictions = None

top_n_by_user = {}

def generate_top_n_for_all_users(users):
    for user_id in users:
        predictions_for_user = predictions[['Item', user_id]]

        predictions_for_user = predictions_for_user.sort_values(by=[user_id], ascending=False)
        top_n_by_user[user_id] = predictions_for_user

def get_ratings(user_id):
    return ratings[['item', user_id]].dropna()


def get_predictions(user_id):
    return predictions[['Item', user_id]].dropna()


def get_top_n(user_id, n):
    return top_n_by_user[user_id].head(n=n)


def get_relevant_items_for_user(user_id):
    user_ratings = get_ratings(user_id)
    return user_ratings[user_ratings[user_id] > 3.0]


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
    ratings = ratings_arg

def set_predictions(predictions_arg):
    global predictions
    global users
    predictions = predictions_arg
    users = users | set(predictions.columns[1:])