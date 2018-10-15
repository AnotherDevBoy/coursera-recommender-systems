import pandas as pd

ratings_df = pd.read_csv('data/ratings.csv')

ALGORITHMS = ['cbf', 'mf', 'item-item']
WEIGHTS = [0.10, 0.25, 0.50, 0.75, 0.85, 0.90, 0.95]

for algorithm_1 in ALGORITHMS:
  algorithm_1_scores_df = pd.read_csv('data/%s.csv' % algorithm_1)
  for algorithm_2 in ALGORITHMS:
    if algorithm_1 != algorithm_2:
      algorithm_2_scores_df = pd.read_csv('data/%s.csv' % algorithm_2)
      for weight in WEIGHTS:
        scores_df = algorithm_1_scores_df.copy()
        other_df = algorithm_2_scores_df.copy()

        common_items = list(set(scores_df['Item']) & set(other_df['Item']))
        common_users = list(set(scores_df.columns[1:]) & set(other_df.columns[1:]))

        for item in common_items:
          index_1 = scores_df.index[scores_df['Item'] == item].tolist()[0]
          index_2 = other_df.index[scores_df['Item'] == item].tolist()[0]

          for user in common_users:
            value_1 = scores_df.at[index_1, user]
            value_2 = other_df.at[index_1, user]
            final_score = value_1*weight + value_2*(1-weight)
            scores_df.set_value(index_1, user, final_score)

        scores_df.to_csv('data/weighted_%s_%d_%s.csv' % (algorithm_1, int(weight*100), algorithm_2), encoding='utf-8', index=False)
