import pandas as pd

def find_cold_start_users(users_with_ratings, max_rating):
  cold_start_users = []

  for user_id in users_with_ratings:
    user_ratings_count = len(ratings_df[user_id].dropna())

    if user_ratings_count <= max_rating:
      cold_start_users.append(user_id)

  return cold_start_users

ratings_df = pd.read_csv('data/ratings.csv')
uu_scores_df = pd.read_csv('data/user-user.csv')

ALGORITHMS = ['cbf', 'mf', 'perbias', 'item-item']
MAX_RATINGS = [10, 11]

users_with_ratings = ratings_df.columns[1:]

for algorithm in ALGORITHMS:
  for max_rating in MAX_RATINGS:
    cold_start_users = find_cold_start_users(users_with_ratings, max_rating)

    alternative_scores_df = pd.read_csv('data/%s.csv' % (algorithm))
    cold_start_cbf_scores_df = alternative_scores_df[['Item'] + cold_start_users]

    uu_scores_df.update(cold_start_cbf_scores_df)

    uu_scores_df.to_csv('data/switch_%s_%s.csv' % (algorithm, max_rating), encoding='utf-8', index=False)
