import pandas as pd
from math import sqrt
import numpy as np   

top_n_by_user = {}

def generate_top_n_for_all_users():
    for user_id in users:
        predictions_for_user = predictions[['Item', user_id]]
        
        predictions_for_user = predictions_for_user.sort_values(by=[user_id], ascending=False)
        top_n_by_user[user_id] = predictions_for_user

def read_items_from_file():
    items_df = pd.read_csv('items.csv')
    items_df = items_df[['Item', 'Availability', 'Price', 'LeafCat', 'FullCat']]

    for item_r in items_df.iterrows():
        item = { 'id': item_r[1]['Item'], 'Availability': item_r[1]['Availability'], 'Price': item_r[1]['Price'] }
        items.append(item)


def get_ratings(user_id):
    return ratings[['item', user_id]].dropna()

def get_predictions(user_id):
    return predictions[['Item', user_id]].dropna()

def get_top_n(user_id, n):
    return top_n_by_user[user_id].head(n=n)

def get_relevant_items_for_user(user_id):
    user_ratings = get_ratings(user_id)
    return user_ratings[user_ratings[user_id] > 3.0]

def mrr():
    mrr = 0.0

    for user_id in users:
        user_relevant_items = get_relevant_items_for_user(user_id)
        top_n = get_top_n(user_id, 5)

        rank = 1.0

        for recommendation in top_n.iterrows():
            if recommendation[1]['Item'] in list(user_relevant_items['item']):
                mrr += 1.0/rank
            
            rank += 1.0

        number_of_users = 1.0 * len(users)

    return  mrr/number_of_users

def rmse_top_n():
    sum_squared_error = 0.0
    total_ratings = 0

    for user_id in users:
        user_ratings = get_ratings(user_id)
        top_n = get_top_n(user_id, 5)

        recommended_and_rated_items = list(set(user_ratings['item']) & set(top_n['Item']))

        if recommended_and_rated_items:
            user_ratings_df = user_ratings[user_ratings['item'].isin(recommended_and_rated_items)]
            top_n_df = top_n[top_n['Item'].isin(recommended_and_rated_items)]

            filtered_user_ratings_values = list(map(float, user_ratings_df[user_id]))
            filtered_top_n_values = list(map(float, top_n_df[user_id]))

            error = np.subtract(filtered_user_ratings_values, filtered_top_n_values)

            squared_error = np.power(error, 2)
            sum_squared_error += np.sum(squared_error)
            total_ratings += len(recommended_and_rated_items)

    return sqrt(sum_squared_error / total_ratings)

def rmse_predict():
    sum_squared_error = 0.0
    total_ratings = 0

    for user_id in users:
        user_ratings = get_ratings(user_id)
        user_predictions = get_predictions(user_id)

        predicted_and_rated_items = list(set(user_ratings['item']) & set(user_predictions['Item']))

        if predicted_and_rated_items:
            user_ratings_df = user_ratings[user_ratings['item'].isin(predicted_and_rated_items)]
            user_predictions_df = user_predictions[user_predictions['Item'].isin(predicted_and_rated_items)]

            filtered_user_ratings_values = list(map(float, user_ratings_df[user_id]))
            filtered_user_predictions_values = list(map(float, user_predictions_df[user_id]))

            error = np.subtract(filtered_user_ratings_values, filtered_user_predictions_values)

            squared_error = np.power(error, 2)
            sum_squared_error += np.sum(squared_error)
            total_ratings += len(predicted_and_rated_items)

    return sqrt(sum_squared_error / total_ratings)

def precision(recommended_items, user_relevant_items):
    recommended_relevant_items = list(set(recommended_items['Item']) & set(user_relevant_items['item']))

    return float(len(recommended_relevant_items)) / float(len(recommended_items['Item']))

def mean_average_precision():
    average_precision = 0.0

    user_id = '64'

    precision_for_user = 0.0
    user_relevant_items = get_relevant_items_for_user(user_id)

    top_n = get_top_n(user_id, 5)
    
    for i in range(len(top_n['Item'])):
        recommended_at_k = get_top_n(user_id, i+1)
        candidate_item = list(top_n['Item'])[i]
        
        if candidate_item in list(user_relevant_items['item']):
            precision_for_user += precision(recommended_at_k, user_relevant_items)
    
    average_precision += precision_for_user / float(len(user_relevant_items))

    return average_precision / float(len(users))

def coverage():
    items_recommended = set()

    for user_id in users:
        top_n = get_top_n(user_id, 5)
        top_n_items = set(top_n['Item'])

        items_recommended = items_recommended | top_n_items

    return float(len(items_recommended))/float(len(items))

def average_availability_by_user():
    availability = 0.0

    for user_id in users:
        availability_for_user = 0.0
        top_n = get_top_n(user_id, 5)

        top_n_items = top_n['Item']

        for top_n_item in top_n_items:
            items_found = [item for item in items if item['id'] == top_n_item]

            availability_for_user += items_found[0]['Availability']

        availability += availability_for_user/float(len(top_n_items))

    return availability/float(len(users))

'''
def intralist_category_diversity():
    # TBD

def intralist_price_diversity():
    # TBD
'''

algorithms = ['cbf.csv', 'item-item.csv', 'mf.csv', 'perbias.csv', 'user-user.csv']

ratings = pd.read_csv('ratings.csv')

items = []
read_items_from_file()

results = { 'MRR': [], 'RMSE.Predict': [], 'RMSE.TopN': [], 'MAP': [], 'Coverage': [], 'Average Availability': [] }

algorithm = algorithms[-1]
print algorithm
#for algorithm in algorithms:
users = pd.read_csv(algorithm, nrows=1).columns[1:] 
predictions = pd.read_csv(algorithm)
generate_top_n_for_all_users()
average_availability_by_user()

results['MRR'].append(mrr())
results['RMSE.Predict'].append(rmse_predict())
results['RMSE.TopN'].append(rmse_top_n())
results['MAP'].append(mean_average_precision())
results['Coverage'].append(coverage())
results['Average Availability'].append(average_availability_by_user())

print results
# result_df = pd.DataFrame(data=results, index=algorithms)
# print result_df