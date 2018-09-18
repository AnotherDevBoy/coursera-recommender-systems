from __future__ import absolute_import

import pandas as pd
from math import sqrt
import numpy as np

from lib.availability import average_availability_by_user
from lib.coverage import item_coverage, user_coverage, category_coverage
from lib.data import *
from lib.diversity import intralist_price_diversity, intralist_category_diversity
from lib.mrr import mrr
from lib.precision import mean_average_precision
from lib.rmse import rmse_top_n, rmse_predict
from lib.utils import read_items_from_file, read_ratings_from_file, read_predictions_from_file, print_items_from_list
from lib.serendipity import serendipity
from lib.ndcg import average_ndcg

pd.set_option('display.max_columns', None)

algorithms = ['cbf', 'item-item', 'mf', 'perbias', 'user-user']

set_ratings(read_ratings_from_file())
items = read_items_from_file()
set_items(items)

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

  results['MRR'].append(mrr(users))
  results['RMSE.Predict'].append(rmse_predict(users))
  results['RMSE.TopN'].append(rmse_top_n(users))
  results['MAP'].append(mean_average_precision(users))
  results['Item Coverage'].append(item_coverage(users, items))
  results['User Coverage'].append(user_coverage(users))
  results['Category Coverage'].append(category_coverage(users, items))
  results['Avg Availability'].append(average_availability_by_user(users))
  results['Avg Price Diversity'].append(intralist_price_diversity(users))
  results['Avg Category Diversity'].append(intralist_category_diversity(users))
  results['Avg Serendipity'].append(serendipity(users))
  results['Avg nDCG'].append(average_ndcg(users))

result_df = pd.DataFrame(data=results, index=algorithms)
print result_df
