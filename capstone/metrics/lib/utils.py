import pandas as pd
import numpy as np

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
    items = []
    items_df = pd.read_csv('data/items.csv')
    items_df = items_df[['Item', 'Availability', 'Price', 'LeafCat', 'FullCat']]

    for item_r in items_df.iterrows():
        price_tag = get_price_tag(item_r[1]['Price'])
        item = { 'id': item_r[1]['Item'], 'Availability': item_r[1]['Availability'], 'Price': item_r[1]['Price'], 'PriceTag': price_tag }
        items.append(item)

    return items

def read_ratings_from_file():
    return pd.read_csv('data/ratings.csv')

def read_predictions_from_file(file):
    predictions_path = 'data/' + file + '.csv'
    return pd.read_csv(predictions_path)

def print_items_from_list(item_list):
    items = []

    for item in item_list:
        items.append(get_item_by_id(item))

    items_df = pd.DataFrame(data=items)
    print items_df