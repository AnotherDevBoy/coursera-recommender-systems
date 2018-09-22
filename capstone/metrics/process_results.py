from __future__ import absolute_import

import pandas as pd
from math import sqrt
import numpy as np

from lib.data import *

from lib.availability import availability_for_user
from lib.coverage import is_user_covered, category_coverage_for_user
from lib.diversity import intralist_price_diversity, intralist_category_diversity
from lib.mrr import mrr_for_user
from lib.precision import mean_average_precision_for_user
from lib.rmse import rmse_top_n, rmse_predict
from lib.utils import read_items_from_file, read_ratings_from_file, read_predictions_from_file, print_items_from_list
from lib.serendipity import serendipity_for_user
from lib.ndcg import average_ndcg

pd.set_option('display.max_columns', None)

algorithms = ['cbf', 'item-item', 'mf', 'perbias', 'user-user']

set_ratings(read_ratings_from_file())
items = read_items_from_file()
set_items(items)
all_categories = set(map(lambda x: x['LeafCat'], items))

results = {
    'MRR': [],
    'RMSE.Predict': [],
    'RMSE.TopN': [],
    'MAP': [],
    'Item Coverage': [],
    'User Coverage': [],
    'Category Coverage': [],
    'Avg Availability': [],
    'Avg Price Diversity': [],
    'Avg Category Diversity': [],
    'Avg Serendipity': [],
    'Avg nDCG': []
}

for algorithm in algorithms:
  predictions = read_predictions_from_file(algorithm)
  set_predictions(predictions)

  users = get_users()
  generate_top_n_for_all_users(users)

  availability_values = []
  items_recommended = set()
  users_covered = 0.0
  covered_categories = set()
  mrr_values = []
  serendipity_values = []
  map_values = []

  for user_id in users:
    top_n = get_top_n(user_id, 5)

    availability_values.append(availability_for_user(top_n))
    items_recommended = items_recommended | set(top_n['Item'])

    if is_user_covered(top_n):
      users_covered += 1.0

    covered_categories = covered_categories | category_coverage_for_user(top_n)
    mrr_values.append(mrr_for_user(top_n, get_relevant_items_for_user(user_id)))
    serendipity_values.append(serendipity_for_user(top_n, user_id))
    map_values.append(mean_average_precision_for_user(top_n, user_id))

  # results['Avg Availability'].append(availability/float(len(users)))
  results['Item Coverage'].append(float(len(items_recommended))/float(len(items)))
  results['User Coverage'].append(users_covered/float(len(users)))
  results['Category Coverage'].append(float(len(covered_categories))/float(len(all_categories)))

  # results['MRR'].append(mrr/float(len(users)))
  # results['MAP'].append(mean_average_precision(users))
  # results['Avg Serendipity'].append(serendipity(users))
'''
  results['RMSE.Predict'].append(rmse_predict(users))
  results['RMSE.TopN'].append(rmse_top_n(users))
  results['Avg Price Diversity'].append(intralist_price_diversity(users))
  results['Avg Category Diversity'].append(intralist_category_diversity(users))
  results['Avg nDCG'].append(average_ndcg(users))
'''

result_df = pd.DataFrame(data=results, index=algorithms)
print result_df
