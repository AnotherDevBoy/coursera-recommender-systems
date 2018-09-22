from data import get_relevant_items_for_user, get_top_n


def precision(recommended_items, user_relevant_items):
  recommended_relevant_items = list(
      set(recommended_items['Item']) & set(user_relevant_items['item']))
  return float(len(recommended_relevant_items)) / float(len(recommended_items['Item']))


def mean_average_precision_for_user(top_n, user_id):
  precision_for_user = 0.0
  user_relevant_items = get_relevant_items_for_user(user_id)

  for i in range(len(top_n['Item'])):
    recommended_at_k = get_top_n(user_id, i+1)
    candidate_item = list(top_n['Item'])[i]

    if candidate_item in list(user_relevant_items['item']):
      precision_for_user += precision(recommended_at_k, user_relevant_items)

  return precision_for_user / float(len(user_relevant_items))
