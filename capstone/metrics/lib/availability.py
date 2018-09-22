from data import get_item_by_id


def availability_for_user(top_n):
  availability_for_user = 0.0
  top_n_items = top_n['Item']

  for top_n_item in top_n_items:
    item = get_item_by_id(top_n_item)
    availability_for_user += item['Availability']

  return availability_for_user
