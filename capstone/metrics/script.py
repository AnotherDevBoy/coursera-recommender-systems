import pandas as pd
from math import sqrt
import numpy as np   

def top_n_for_user(predictions, user_id, n):
    predictions_for_user = predictions[[user_id]]
    predictions_for_user = predictions_for_user.sort_values(by=[user_id], ascending=False)
    return predictions_for_user.head(n=n)

def mrr(ratings, predictions):
    mrr = 0.0

    for user_id in users:
        user_ratings = ratings[user_id].dropna()
        top_n = top_n_for_user(predictions, user_id, 5)

        rank = 1.0

        for recommendation in top_n.iterrows():
            recommended_item =  recommendation[0]

            if recommended_item in user_ratings:
                mrr += 1/rank
            
            rank += 1.0

    number_of_users = 1.0 * len(users)

    return  mrr/number_of_users

def rmse(ratings, predictions):
    sum_squared_error = 0.0
    total_ratings = 0

    for user_id in users:
        user_ratings = ratings[user_id].dropna()
        top_n = top_n_for_user(predictions, user_id, 5)

        recommended_relevant_items = list(set(user_ratings.index) & set(top_n.index))

        filtered_top_n_df = top_n.filter(items=recommended_relevant_items, axis=0)
        filtered_user_ratings_df = user_ratings.filter(items=recommended_relevant_items, axis=0)

        filtered_top_n_values = list(map(float, filtered_top_n_df[user_id]))
        filtered_user_ratings_values = list(map(float, filtered_user_ratings_df))

        error = np.subtract(filtered_top_n_values, filtered_user_ratings_values)
        squared_error = np.power(error, 2)
        sum_squared_error += np.sum(squared_error)
        total_ratings += len(user_ratings)

    return sqrt(sum_squared_error / total_ratings)

def precision(recommended_items, user_relevant_items):
    recommended_relevant_items = list(set(user_relevant_items.index) & set(recommended_items.index))

    return float(len(recommended_relevant_items)) / float(len(recommended_items))

def mean_average_precision(ratings, predictions):
    user_id = '64'

    average_precision = 0.0

    for user_id in users:
        precision_for_user = 0.0
        user_relevant_items = ratings[ratings[user_id] > 3.0][user_id].dropna()

        top_n = top_n_for_user(predictions, user_id, 5)
        
        for i in range(len(top_n.index)):
            recommended_at_k = top_n_for_user(predictions, user_id, i+1)
            candidate_item = list(top_n.index)[i]
            
            if candidate_item in list(user_relevant_items.index):
                precision_for_user += precision(recommended_at_k, user_relevant_items)
        
        average_precision += precision_for_user / float(len(user_relevant_items))

    return average_precision / float(len(users))

def coverage(ratings, predictions):
    # TBD

def intralist_category_diversity(ratings, predictions):
    # TBD

def intralist_price_diversity(ratings, predictions):
    # TBD


users = pd.read_csv('cbf.csv', nrows=1).columns[1:] 
predictions = pd.read_csv('cbf.csv')
ratings = pd.read_csv('ratings.csv')

print 'MRR', mrr(ratings, predictions), 'RMSE', rmse(ratings, predictions), 'MAP', mean_average_precision(ratings, predictions)