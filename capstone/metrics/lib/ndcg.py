import numpy as np
from data import is_item_relevant_for_user


def log_discount(ranking):
  return np.log2(ranking+1)


def max_dcg(number_of_items, max_rating):
  total_max_dcg = 0.0

  for rank in range(number_of_items):
    total_max_dcg += max_rating/log_discount(rank+1)

  return total_max_dcg


def ndcg(user_id, top_n):
  dcg = 0.0

  ranking = 1.0
  for recommendation in top_n.iterrows():
    if is_item_relevant_for_user(user_id, recommendation[1]['Item']):
      prediction = recommendation[1][user_id]
      dcg += prediction/log_discount(ranking)

    ranking += 1.0

  return dcg/max_dcg(len(top_n), 5.0)
