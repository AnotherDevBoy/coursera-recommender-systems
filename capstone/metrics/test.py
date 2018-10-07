import numpy as np
import pandas as pd

from lib.data import generate_top_n_for_all_users, get_ratings, get_predictions, get_top_n, rerank_top_n, get_relevant_items_for_user, set_items, get_users, set_ratings, set_predictions

# Metric Imports
from lib.availability import availability_for_user
from lib.coverage import is_user_covered, category_coverage_for_user
from lib.diversity import intralist_price_diversity_for_user, intralist_category_diversity_for_user
from lib.mrr import mrr_for_user
from lib.precision import average_precision_for_user
from lib.rmse import rmse_for_user
from lib.serendipity import serendipity_for_user
from lib.ndcg import ndcg

from lib.utils import read_items_from_file, read_ratings_from_file, read_predictions_from_file, calculate_statistics, generate_output_files

set_ratings(read_ratings_from_file())
ITEMS = read_items_from_file()
set_items(ITEMS)
predictions = read_predictions_from_file('user-user')
set_predictions(predictions)

users = get_users()
generate_top_n_for_all_users(users)

top_n = get_top_n('804', 5)
print top_n
print rerank_top_n('804', top_n, 3)
