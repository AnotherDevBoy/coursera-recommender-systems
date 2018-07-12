import pandas as pd
from math import sqrt
import numpy as np   
from sklearn.metrics import mean_squared_error, average_precision_score, precision_score

top_n_by_user = {}

def generate_top_n_for_all_users():
    for user_id in users:
        predictions_for_user = predictions[['Item', user_id]]
        
        predictions_for_user = predictions_for_user.sort_values(by=[user_id], ascending=False)
        top_n_by_user[user_id] = predictions_for_user


# TODO: Define more accurate ranges based on price distribution
def get_price_tag(price):
    if np.isnan(price):
        return 'Unknown'

    if price >= 0.000000 and price < 1.0:
        return 'Super Cheap'

    if price >= 1.0 and price < 5.0:
        return 'Cheap'

    if price >= 5.0 and price < 50.0:
        return 'Affordable'

    if price >= 50.0 and price < 150.0:
        return 'Pricy'

    if price >= 150.0 and price < 300.0:
        return 'Expensive'

    if price >= 300.0 and price < 500.0:
        return 'Quite Expensive'

    return 'Really Expensive'
        

def read_items_from_file():
    items_df = pd.read_csv('items.csv')
    items_df = items_df[['Item', 'Availability', 'Price', 'LeafCat', 'FullCat']]

    for item_r in items_df.iterrows():
        price_tag = get_price_tag(item_r[1]['Price'])
        item = { 'id': item_r[1]['Item'], 'Availability': item_r[1]['Availability'], 'Price': item_r[1]['Price'], 'PriceTag': price_tag }
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


def get_item_by_id(item_id):
    items_found = [item for item in items if item['id'] == item_id]

    if items_found:
        return items_found[0]

    return -1


def mrr():
    mrr = 0.0

    for user_id in users:
        user_relevant_items = get_relevant_items_for_user(user_id)
        top_n = get_top_n(user_id, 5)

        rank = 1.0

        for recommendation in top_n.iterrows():
            if recommendation[1]['Item'] in list(user_relevant_items['item']):
                mrr += 1.0/float(rank)
            
            rank += 1.0

        number_of_users = float(len(users))

    return  mrr/number_of_users


def rmse(get_predicted_values, *argv):
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

def rmse_top_n():
    return rmse(get_top_n, 5)


def rmse_predict():
    return rmse(get_predictions)


def precision(recommended_items, user_relevant_items):
    recommended_relevant_items = list(set(recommended_items['Item']) & set(user_relevant_items['item']))
    return float(len(recommended_relevant_items)) / float(len(recommended_items['Item']))


def mean_average_precision():
    average_precision = 0.0

    for user_id in users:
        user_relevant_items = get_relevant_items_for_user(user_id)
        top_n = get_top_n(user_id, 5)

        precision_for_user = 0.0
        
        for i in range(len(top_n['Item'])):
            recommended_at_k = get_top_n(user_id, i+1)
            candidate_item = list(top_n['Item'])[i]
            
            if candidate_item in list(user_relevant_items['item']):
                precision_for_user += precision(recommended_at_k, user_relevant_items)
        
        average_precision += precision_for_user / float(len(user_relevant_items))

    return average_precision / float(len(users))


def item_coverage():
    items_recommended = set()

    for user_id in users:
        top_n = get_top_n(user_id, 5)
        top_n_items = set(top_n['Item'])

        items_recommended = items_recommended | top_n_items

    return float(len(items_recommended))/float(len(items))


def user_coverage():
    users_covered = 0.0

    for user_id in users:
        top_n = get_top_n(user_id, 5)
        top_n_items = set(top_n['Item'])

        if top_n_items:
            users_covered += 1.0

    return users_covered/float(len(users))


def average_availability_by_user():
    availability = 0.0

    for user_id in users:
        availability_for_user = 0.0
        top_n = get_top_n(user_id, 5)

        top_n_items = top_n['Item']

        for top_n_item in top_n_items:
            item = get_item_by_id(top_n_item)
            availability_for_user += item['Availability']

        availability += availability_for_user/float(len(top_n_items))

    return availability/float(len(users))


def intralist_price_diversity():
    average_disimilarity = 0.0

    for user_id in users:
        top_n = get_top_n(user_id, 5)
        top_n_items = top_n['Item']

        overall_disimilarity = 0.0
        for item_i_id in top_n_items:
            disimilarity = 0.0
            for item_j_id in top_n_items:
                if item_i_id != item_j_id:
                    item_i = get_item_by_id(item_i_id)
                    item_j = get_item_by_id(item_j_id)
                    if item_i['PriceTag'] != 'Unknown' and item_j['PriceTag'] != 'Unknown' and item_i['PriceTag'] != item_j['PriceTag']:
                        disimilarity += 1
            
            overall_disimilarity += disimilarity/float(len(top_n_items))
        
        disimilarity_per_user = overall_disimilarity/float(len(top_n_items))
        average_disimilarity += disimilarity_per_user

    return average_disimilarity/float(len(users))


def print_items_from_list(item_list):
    items = []

    for item in item_list:
        items.append(get_item_by_id(item))
    
    items_df = pd.DataFrame(data=items)
    print items_df

'''
def intralist_category_diversity():
    # TBD
'''

algorithms = ['cbf.csv', 'item-item.csv', 'mf.csv', 'perbias.csv', 'user-user.csv']

ratings = pd.read_csv('ratings.csv')

items = []
read_items_from_file()

results = { 'MRR': [], 'RMSE.Predict': [], 'RMSE.TopN': [], 'MAP': [], 'Item Coverage': [], 'User Coverage': [], 'Avg Availability': [], 'Avg Price Diversity': [] }

algorithm = algorithms[-1]
for algorithm in algorithms:
    users = pd.read_csv(algorithm, nrows=1).columns[1:] 
    predictions = pd.read_csv(algorithm)
    generate_top_n_for_all_users()
    average_availability_by_user()

    results['MRR'].append(mrr())
    results['RMSE.Predict'].append(rmse_predict())
    results['RMSE.TopN'].append(rmse_top_n())
    results['MAP'].append(mean_average_precision())
    results['Item Coverage'].append(item_coverage())
    results['User Coverage'].append(user_coverage())
    results['Avg Availability'].append(average_availability_by_user())
    results['Avg Price Diversity'].append(intralist_price_diversity())

result_df = pd.DataFrame(data=results, index=algorithms)
print result_df