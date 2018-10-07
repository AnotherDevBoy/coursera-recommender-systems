from data import get_relevant_items_for_user, get_top_n

# https://medium.com/@m_n_malaeb/recall-and-precision-at-k-for-recommender-systems-618483226c54


def _recall(top_n, user_id):
  top_n_items = set(top_n['Item'])
  user_relevant_items = set(get_relevant_items_for_user(user_id)['item'])

  recommended_and_relevant = top_n_items & user_relevant_items

  total_relevant_items = len(user_relevant_items)
  if total_relevant_items > 0:
    return float(len(recommended_and_relevant))/float(total_relevant_items)

  return 0.0


def _precision(top_n, user_id):
  top_n_items = set(top_n['Item'])
  user_relevant_items = set(get_relevant_items_for_user(user_id)['item'])

  recommended_and_relevant = top_n_items & user_relevant_items

  total_recommended = len(top_n_items)
  if total_recommended > 0:
    return float(len(recommended_and_relevant))/float(total_recommended)

  return 0.0

def f1_score(top_n, user_id):
  precision = _precision(top_n, user_id)
  recall = _recall(top_n, user_id)

  if precision+recall > 0:
    return 2.0*(precision*recall)/(precision+recall)

  return 0.0

def average_precision_for_user(top_n, user_id):
  average_precision = 0.0

  top_n_items = list(top_n['Item'])
  user_relevant_items = list(get_relevant_items_for_user(user_id)['item'])

  relevant_items_count = 0
  for i in range(len(top_n['Item'])):
    rank = i + 1
    if top_n_items[i] in user_relevant_items:
      relevant_items_count += 1
      precision = float(relevant_items_count)/float(rank)
      average_precision += precision

  if relevant_items_count > 0:
    return average_precision/float(relevant_items_count)

  return 0.0
