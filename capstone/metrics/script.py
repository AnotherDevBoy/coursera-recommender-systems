import pandas as pd

def mrr(ratings, top_n):
    mrr = 0.0
    for user_id in users:
        user_ratings = ratings[user_id].dropna()

        rank = 1.0

        for recommendation in top_n.iterrows():
            recommended_item =  recommendation[0]

            if recommended_item in user_ratings:
                mrr += 1/rank
                print 'User', user_id, 'rated item', recommended_item, 'rank', rank
            
            rank += 1.0

    number_of_users = 1.0 * len(users)

    return  mrr/number_of_users

headers = pd.read_csv('cbf.csv', nrows=1)

users = headers.columns[1:] 

predictions = pd.read_csv('cbf.csv')

ratings = pd.read_csv('ratings.csv')

user_id = '64'

predictions_for_user = predictions[[user_id]]
predictions_for_user = predictions_for_user.sort_values(by=[user_id], ascending=False)
top_n = predictions_for_user.head()

print 'MRR', mrr(ratings, top_n)