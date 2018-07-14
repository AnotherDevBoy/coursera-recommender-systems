import pandas as pd
import numpy as np

from data import get_top_n, get_item_by_id

def intralist_field_diversity(users, field):
    average_disimilarity = 0.0

    for user_id in users:
        top_n = get_top_n(user_id, 5)
        top_n_items = top_n['Item']

        overall_disimilarity = 0.0
        for item_i_id in top_n_items:
            disimilarity = 0.0
            for item_j_id in top_n_items:
                if item_i_id != item_j_id:
                    item_i = get_item_by_id(item_i_id)
                    item_j = get_item_by_id(item_j_id)
                    if item_i[field] and item_i[field] != 'Unknown' and item_j[field] and item_j[field] != 'Unknown' and item_i[field] != item_j[field]:
                        disimilarity += 1.0

            overall_disimilarity += disimilarity/float(len(top_n_items))

        disimilarity_per_user = overall_disimilarity/float(len(top_n_items))
        average_disimilarity += disimilarity_per_user

    return average_disimilarity/float(len(users))

def intralist_price_diversity(users):
    return intralist_field_diversity(users, 'PriceTag')

def intralist_leafcategory_diversity(users):
    return intralist_field_diversity(users, 'LeafCat')


'''
def intralist_category_diversity():
    # TBD
'''