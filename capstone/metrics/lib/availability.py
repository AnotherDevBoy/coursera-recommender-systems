from data import get_item_field_by_id


def availability_for_user(top_n):
  availability_for_user = 0.0

  for item_id in top_n['Item']:
    availability_for_user += get_item_field_by_id(item_id, 'Availability')

  return availability_for_user/len(top_n['Item'])
