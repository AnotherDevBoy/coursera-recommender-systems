
from data import is_item_relevant_for_user, is_item_popular


def serendipity_for_user(top_n, user_id):
  top_n_serendipity = 0.0
  top_n_items = set(top_n['Item'])

  for item_id in top_n_items:
    if is_item_relevant_for_user(user_id, item_id) and not is_item_popular(item_id):
      top_n_serendipity += 1.0

  if len(top_n_items) > 0:
    return top_n_serendipity/float(len(top_n_items))

  return 0.0
