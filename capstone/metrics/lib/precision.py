from data import get_relevant_items_for_user, get_top_n


def average_precision_for_user(top_n, user_id):
  average_precision = 0.0

  top_n_items = list(top_n['Item'])
  user_relevant_items = list(get_relevant_items_for_user(user_id)['item'])

  for i in range(len(top_n['Item'])):
    relevant_items_count = 0
    rank = i + 1
    if top_n_items[i] in user_relevant_items:
      relevant_items_count += 1
      average_precision += relevant_items_count/rank

  if relevant_items_count > 0:
    return average_precision/relevant_items_count

  return 0
