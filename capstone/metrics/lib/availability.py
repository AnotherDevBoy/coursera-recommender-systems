from data import get_top_n, get_item_by_id


def average_availability_by_user(users):
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
