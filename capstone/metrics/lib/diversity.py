import numpy as np

from data import get_item_field_by_id

def intralist_diversity_for_user(top_n, field):
  top_n_items = top_n['Item']

  overall_disimilarity = 0.0
  for item_i_id in top_n_items:
    disimilarity = 0.0
    for item_j_id in top_n_items:
      if item_i_id != item_j_id:
        field_i = get_item_field_by_id(item_i_id, field)
        field_j = get_item_field_by_id(item_j_id, field)
        if field_i and field_i != 'Unknown' and field_j and field_j != 'Unknown' and field_i != field_j:
          disimilarity += 1.0

    overall_disimilarity += disimilarity/float(len(top_n_items))

  return overall_disimilarity/float(len(top_n_items))


def intralist_price_diversity_for_user(top_n):
  return intralist_diversity_for_user(top_n, 'PriceTag')

def intralist_category_diversity_for_user(top_n):
  return intralist_diversity_for_user(top_n, 'LeafCat')
