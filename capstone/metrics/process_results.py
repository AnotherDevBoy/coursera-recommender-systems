from __future__ import absolute_import

import time

from lib.data import *

# Metric Imports
from lib.availability import availability_for_user
from lib.coverage import is_user_covered, category_coverage_for_user
from lib.diversity import intralist_price_diversity_for_user, intralist_category_diversity_for_user
from lib.mrr import mrr_for_user
from lib.precision import mean_average_precision_for_user
from lib.rmse import rmse_for_user
from lib.serendipity import serendipity_for_user
from lib.ndcg import ndcg

from lib.utils import read_items_from_file, read_ratings_from_file, read_predictions_from_file

algorithms = ['cbf', 'item-item', 'mf', 'perbias', 'user-user']

set_ratings(read_ratings_from_file())
ITEMS = read_items_from_file()
set_items(ITEMS)
ALL_CATEGORIES = set(map(lambda x: x['LeafCat'], ITEMS))

results = {}

start_time = time.time()

for algorithm in algorithms:
  results[algorithm] = {}
  predictions = read_predictions_from_file(algorithm)
  set_predictions(predictions)

  users = get_users()
  generate_top_n_for_all_users(users)

  items_recommended = set()
  users_covered = 0.0
  covered_categories = set()

  results[algorithm]['Availability'] = []
  results[algorithm]['MRR'] = []
  results[algorithm]['Serendipity'] = []
  results[algorithm]['MAP'] = []
  results[algorithm]['RMSE.Predict'] = []
  results[algorithm]['RMSE.TopN'] = []
  results[algorithm]['nDCG'] = []
  results[algorithm]['Diversity.Price'] = []
  results[algorithm]['Diversity.Category'] = []

  for user_id in users:
    top_n = get_top_n(user_id, 5)
    user_ratings = get_ratings(user_id)
    user_relevant_items = get_relevant_items_for_user(user_id)
    user_predictions = get_predictions(user_id)

    # Coverage Metrics
    items_recommended = items_recommended | set(top_n['Item'])

    if is_user_covered(top_n):
      users_covered += 1.0

    covered_categories = covered_categories | category_coverage_for_user(top_n)

    results[algorithm]['Coverage.Item'] = float(len(items_recommended))/float(len(ITEMS))
    results[algorithm]['Coverage.User'] = users_covered/float(len(users))
    results[algorithm]['Coverage.Category'] = float(len(covered_categories))/float(len(ALL_CATEGORIES))

    # Other metrics
    results[algorithm]['Availability'].append(availability_for_user(top_n))
    results[algorithm]['MRR'].append(mrr_for_user(top_n, user_relevant_items))
    results[algorithm]['Serendipity'].append(serendipity_for_user(top_n, user_id))
    results[algorithm]['MAP'].append(mean_average_precision_for_user(top_n, user_id))
    results[algorithm]['RMSE.Predict'].append(rmse_for_user(user_id, user_ratings, user_predictions))
    results[algorithm]['RMSE.TopN'].append(rmse_for_user(user_id, user_ratings, top_n))
    results[algorithm]['nDCG'].append(ndcg(user_id, top_n))
    results[algorithm]['Diversity.Price'].append(intralist_price_diversity_for_user(top_n))
    results[algorithm]['Diversity.Category'].append(intralist_category_diversity_for_user(top_n))

elapsed_time = time.time() - start_time
print 'Time taken: ', elapsed_time
