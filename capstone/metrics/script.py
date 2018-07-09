import pandas as pd

headers = pd.read_csv("cbf.csv", nrows=1)

users = headers.columns[1:] 

predictions = pd.read_csv("cbf.csv")


for user_id in users:
    predictions_for_user = predictions[[user_id]]
    predictions_for_user = predictions_for_user.sort_values(by=[user_id], ascending=False)
    top_n = predictions_for_user.head()

    print top_n

    

'''
predictions_by_user = {}

for index, prediction in predictions.iterrows():
    item_id = prediction['Item']

    for user in users:
        if not user in predictions_by_user:
            predictions_by_user[user] = []
            
        predictions_by_user[user].append({ 'item': item_id, 'value': prediction[user]})

print predictions_by_user['64']
'''