from utils import *

import pandas as pd

items = []
users = set()
ratings = None
predictions = None
top_n_by_user = {}
items_popularity = {}
ratings_distribution = {}
cold_users = []

#########################################################################
# Generators
#########################################################################


def generate_top_n_for_all_users(users):
  for user_id in users:
    predictions_for_user = predictions[['Item', user_id]]

    predictions_for_user = predictions_for_user.sort_values(
        by=[user_id], ascending=False)
    top_n_by_user[user_id] = predictions_for_user


#########################################################################
# Getters and Setters
#########################################################################


def set_predictions(predictions_arg):
  global predictions
  global users
  global ratings_distribution
  global cold_users
  predictions = predictions_arg
  users = users | set(predictions.columns[1:])

def set_ratings(ratings_arg, cold_max_number_of_ratings=10):
  global ratings
  global items_popularity
  ratings = ratings_arg

  users_that_rated = list(ratings)[1:]
  for _, rating in ratings.iterrows():
    item = rating['item']
    ratings_for_item = 0
    for user in users_that_rated:
      if not np.isnan(rating[user]):
        ratings_for_item += 1

    popularity = float(ratings_for_item)/float(len(users_that_rated))
    items_popularity[item] = popularity

  for user_id in users_that_rated:
    ratings_count = len(ratings[user_id].dropna())

    if ratings_count in ratings_distribution:
      ratings_distribution[ratings_count] += 1
    else:
      ratings_distribution[ratings_count] = 1

    if ratings_count <= cold_max_number_of_ratings:
      cold_users.append(user_id)


def set_items(items_arg):
  global items
  items = items_arg


def get_items():
  return items


def get_users():
  return users


def get_cold_users():
  return cold_users


def get_ratings_distribution():
  return ratings_distribution

def get_ratings(user_id):
  return ratings[['item', user_id]].dropna()


def get_predictions(user_id):
  return predictions[['Item', user_id]].dropna()


def get_top_n(user_id, n):
  return top_n_by_user[user_id].head(n=n)


def get_relevant_items_for_user(user_id):
  user_ratings = get_ratings(user_id)
  average_rating = _get_average_user_rating(user_id)
  return user_ratings[user_ratings[user_id] >= average_rating]


def get_item_field_by_id(item_id, field):
  items_found = [item for item in items if item['id'] == item_id]

  if items_found:
    return items_found[0][field]

  return None

#########################################################################
# Popularity/Relevancy checks
#########################################################################


def is_item_relevant_for_user(user_id, item_id):
  user_rating = get_ratings_for_item(user_id, item_id)

  if not user_rating:
    return False

  return user_rating > 3.0


def is_item_popular(item_id):
  return items_popularity[item_id] >= 0.15


def get_ratings_for_item(user_id, item_id):
  user_ratings = get_ratings(user_id)

  rating = user_ratings.loc[user_ratings['item'] == int(item_id)]

  if rating.empty:
    return None

  return rating.iloc[0][user_id]


def _get_average_user_rating(user_id):
  user_ratings = get_ratings(user_id)
  user_rating_values = list(user_ratings[user_id])

  average_rating = 0.0

  for rating in user_rating_values:
    average_rating += rating

  return average_rating/float(len(user_rating_values))
