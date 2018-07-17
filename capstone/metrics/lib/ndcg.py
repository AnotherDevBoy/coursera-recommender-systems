import numpy as np
from data import get_top_n, is_item_relevant_for_user, get_ratings_for_item

def log_discount(ranking):
    return np.log2(ranking+1)


def max_dcg(number_of_items, max_rating):
    total_max_dcg = 0.0

    for rank in range(number_of_items):
        total_max_dcg += max_rating/log_discount(rank+1)

    return total_max_dcg

cached_max_ndcg = max_dcg(5, 5.0)


def dcg(user_id):
    top_n = get_top_n(user_id, 5).dropna()

    total_dcg = 0.0

    ranking = 1.0
    for recommendation in top_n.iterrows():
        if is_item_relevant_for_user(user_id, recommendation[1]['Item']):
            prediction = recommendation[1][user_id]
            total_dcg += prediction/log_discount(ranking)

        ranking += 1.0

    return total_dcg


def ndcg(user_id):
    dcg_val = dcg(user_id)
    return dcg(user_id)/cached_max_ndcg


def average_ndcg(users):
    total_ndcg = 0.0
    for user_id in users:
        ndcg_val = ndcg(user_id)

        total_ndcg += ndcg_val

    return total_ndcg/float(len(users))