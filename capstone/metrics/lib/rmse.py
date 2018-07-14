from math import sqrt
import numpy as np
from sklearn.metrics import mean_squared_error, average_precision_score, precision_score
from data import get_top_n, get_predictions, get_ratings

def rmse(users, get_predicted_values, *argv):
    good_values = np.array([])
    predicted_values = np.array([])

    for user_id in users:
        user_ratings = get_ratings(user_id)

        user_predictions = get_predicted_values(user_id, argv[0]) if argv else get_predicted_values(user_id)

        predicted_and_rated_items = list(set(user_ratings['item']) & set(user_predictions['Item']))

        if predicted_and_rated_items:
            user_ratings_df = user_ratings[user_ratings['item'].isin(predicted_and_rated_items)]
            user_predictions_df = user_predictions[user_predictions['Item'].isin(predicted_and_rated_items)]
            good_values = np.append(good_values, np.array(user_ratings_df[user_id]))
            predicted_values = np.append(predicted_values, np.array(user_predictions_df[user_id]))

    return sqrt(mean_squared_error(good_values, predicted_values))

def rmse_top_n(users):
    return rmse(users, get_top_n, 5)


def rmse_predict(users):
    return rmse(users, get_predictions)