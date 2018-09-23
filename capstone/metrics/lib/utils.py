import pandas as pd
import numpy as np


def get_price_tag(price):
  if np.isnan(price):
    return 'Unknown'

  if price >= 0.000000 and price < 5.0:
    return 'Cheap'

  if price >= 5.0 and price < 20.0:
    return 'Affordable'

  if price >= 20.0 and price < 50.0:
    return 'Pricy'

  if price >= 50.0 and price < 100.0:
    return 'Expensive'

  return 'Really Expensive'


def read_items_from_file():
  items = []
  items_df = pd.read_csv('data/items.csv')
  items_df = items_df[['Item', 'Availability', 'Price', 'LeafCat', 'FullCat']]

  for item_r in items_df.iterrows():
    price_tag = get_price_tag(item_r[1]['Price'])
    items.append({
      'id': item_r[1]['Item'],
      'Availability': item_r[1]['Availability'],
      'Price': item_r[1]['Price'],
      'PriceTag': price_tag,
      'LeafCat': item_r[1]['LeafCat']
    })

  return items


def read_ratings_from_file():
  return pd.read_csv('data/ratings.csv')


def read_predictions_from_file(file):
  predictions_path = 'data/' + file + '.csv'
  return pd.read_csv(predictions_path)


def calculate_statistics(values):
  np_values = np.array(values)

  return {
    'min': np_values.min(),
    'max': np_values.max(),
    'mean': np_values.mean(),
    '10': np.percentile(np_values, 10),
    '25': np.percentile(np_values, 25),
    '50': np.percentile(np_values, 50),
    '75': np.percentile(np_values, 75),
    '95': np.percentile(np_values, 95),
  }

def generate_output_files(results, metricName):
  filename = './output/%s.csv' % (metricName)

  df = pd.DataFrame.from_dict(results[metricName])
  df.to_csv(filename, encoding='utf-8')
