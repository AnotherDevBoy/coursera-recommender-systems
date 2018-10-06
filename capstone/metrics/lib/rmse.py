from math import sqrt
import sys
import numpy as np
from sklearn.metrics import mean_squared_error


def rmse_for_user(user_id, user_ratings, user_predictions):
  good_values = np.array([])
  predicted_values = np.array([])

  predicted_and_rated_items = list(set(user_ratings['item']) & set(user_predictions['Item']))

  if predicted_and_rated_items:
    user_ratings_df = user_ratings[user_ratings['item'].isin(predicted_and_rated_items)]
    user_predictions_df = user_predictions[user_predictions['Item'].isin(predicted_and_rated_items)]
    good_values = np.append(good_values, np.array(user_ratings_df[user_id]))
    predicted_values = np.append(predicted_values, np.array(user_predictions_df[user_id]))
    return sqrt(mean_squared_error(good_values, predicted_values))

  # If the user has not rated any of the predicted items, then RMSE is technically 0
  return 0
