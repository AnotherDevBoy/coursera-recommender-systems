import pandas as pd

def find_users_to_switch(users_with_ratings, max_rating):
  cold_start_users = []

  for user_id in users_with_ratings:
    user_ratings_count = len(ratings_df[user_id].dropna())

    if user_ratings_count <= max_rating:
      cold_start_users.append(user_id)

  return cold_start_users

ratings_df = pd.read_csv('data/ratings.csv')

ALGORITHMS = ['cbf', 'mf', 'item-item']
MAX_RATINGS = [10, 20, 30]

users_with_ratings = ratings_df.columns[1:]

for algorithm_1 in ALGORITHMS:
  algorithm_1_scores_df = pd.read_csv('data/%s.csv' % algorithm_1)
  for algorithm_2 in ALGORITHMS:
    if algorithm_1 != algorithm_2:
      for max_rating in MAX_RATINGS:
        users_to_switch = find_users_to_switch(users_with_ratings, max_rating)

        algorithm_2_scores_df = pd.read_csv('data/%s.csv' % algorithm_2)
        filtered_algorithm_2_scores_df = algorithm_2_scores_df[['Item'] + users_to_switch]

        algorithm_1_scores_df.update(filtered_algorithm_2_scores_df)

        algorithm_1_scores_df.to_csv('data/switch_%s_%s_%s.csv' % (algorithm_2, max_rating, algorithm_1), encoding='utf-8', index=False)
