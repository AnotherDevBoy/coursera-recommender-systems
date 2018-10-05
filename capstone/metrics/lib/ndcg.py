import numpy as np
from data import is_item_relevant_for_user


def dcg(ratings):
  dcg = 0.0

  for rank in range(len(ratings)):
    dcg += ratings[rank]/np.log2(rank+2)

  return dcg


def ndcg(user_id, top_n):
  max_dcg = dcg(np.repeat(5.0, len(top_n)))

  ratings = []

  for recommendation in top_n.iterrows():
    if is_item_relevant_for_user(user_id, recommendation[1]['Item']):
      ratings.append(recommendation[1][user_id])
    else:
      ratings.append(0.0)

  '''
  for rank in range(1, number_of_items+1):
    recommendation = top_n.loc[rank-1]
    if is_item_relevant_for_user(user_id, recommendation[1]['Item']):
      prediction = recommendation[1][user_id]
      dcg += prediction/np.log2(rank+1)
  '''

  return dcg(ratings)/max_dcg
