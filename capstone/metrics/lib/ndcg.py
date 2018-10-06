import numpy as np
from data import get_ratings_for_item


def dcg(ratings):
  dcg = 0.0

  for i in range(len(ratings)):
    rank = i + 1

    if rank <= 2:
      dcg += ratings[i]
    else:
      dcg += ratings[i]/np.log2(i)

  return dcg


def ndcg(user_id, top_n):
  ratings = []

  for recommendation in top_n.iterrows():
    rating = get_ratings_for_item(user_id, recommendation[1]['Item'])

    if rating:
      ratings.append(rating)
    else:
      ratings.append(0.0)

  return dcg(ratings)/dcg(np.repeat(5.0, len(top_n)))
