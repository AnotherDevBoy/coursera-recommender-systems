from utils import *

import pandas as pd

items = []
users = set()
ratings = None
predictions = None
top_n_by_user = {}
cold_users = []
popular_items = []

#########################################################################
# Generators
#########################################################################


def generate_top_n_for_all_users(users):
  for user_id in users:
    predictions_for_user = predictions[['Item', user_id]]

    sorted_predictions = predictions_for_user.sort_values(by=[user_id], ascending=False)
    top_n_by_user[user_id] = sorted_predictions


#########################################################################
# Getters and Setters
#########################################################################


def set_predictions(predictions_arg):
  global predictions
  predictions = predictions_arg

def set_ratings(ratings_arg, min_number_of_ratings=None, max_number_of_ratings=None):
  global ratings
  global popular_items
  global users

  ratings = ratings_arg
  ratings.rename(columns={'item': 'Item'}, inplace=True)

  ratings_distribution = dict(ratings.count()[1:])

  users = set(ratings.columns[1:])

  # TODO: check how to do this in Python
  if not min_number_of_ratings is None and max_number_of_ratings is None:
    users = { user_id: count for user_id, count in ratings_distribution.iteritems() if count >= min_number_of_ratings and count <= max_number_of_ratings }.keys()
  elif not min_number_of_ratings is None:
    users = { user_id: count for user_id, count in ratings_distribution.iteritems() if count >= min_number_of_ratings }.keys()
  else:
    users = { user_id: count for user_id, count in ratings_distribution.iteritems() if count <= max_number_of_ratings }.keys()

  print users

  for key, value in ratings_distribution.items():
    if value > 15:
        popular_items.append(key)

def set_items(items_arg):
  global items
  items = items_arg


def get_items():
  return items


def get_users():
  return users


def get_cold_users():
  return cold_users

def get_ratings(user_id):
  return ratings[['Item', user_id]].dropna()


def get_predictions(user_id):
  return predictions[['Item', user_id]].dropna()


def get_top_n(user_id, n):
  return top_n_by_user[user_id].head(n=n).reset_index(drop=True)


def rerank_top_n(user_id, top_n, min_relevant_items):
  relevant_items = get_relevant_items_for_user(user_id)
  recommended_relevant_items = set(top_n['Item']) & set(relevant_items['Item'])

  new_top_n = pd.DataFrame()

  not_recommended_relevant_items = relevant_items.loc[~relevant_items['Item'].isin(recommended_relevant_items)]

  items_to_add = min_relevant_items - len(recommended_relevant_items)

  # Accounting for those relevant items that might get pushed out
  # TODO: transform into functional style: filter + count
  for item in set(top_n.tail(n=items_to_add)['Item']):
    if item in set(relevant_items['Item']):
      items_to_add += 1

  new_top_n = pd.concat([new_top_n, not_recommended_relevant_items.head(n=items_to_add)]).reset_index(drop=True)
  new_top_n = pd.concat([new_top_n, top_n]).reset_index(drop=True)
  new_top_n = new_top_n.drop_duplicates(subset='Item')

  return new_top_n.head(n=len(top_n)).reset_index(drop=True)

def get_relevant_items_for_user(user_id):
  user_ratings = get_ratings(user_id)
  average_rating = _get_average_user_rating(user_id)
  relevant_items = user_ratings[user_ratings[user_id] >= average_rating].reset_index(drop=True)
  sorted_relevant_items = relevant_items.sort_values(by=[user_id], ascending=False)
  return sorted_relevant_items


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

  return user_rating >= _get_average_user_rating(user_id)


def is_item_popular(item_id):
  global popular_items
  return item_id in popular_items


def get_ratings_for_item(user_id, item_id):
  user_ratings = get_ratings(user_id)

  rating = user_ratings.loc[user_ratings['Item'] == int(item_id)]

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
