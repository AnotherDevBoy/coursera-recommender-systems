from data import get_top_n, get_item_by_id


def item_coverage(users, items):
  items_recommended = set()

  for user_id in users:
    top_n = get_top_n(user_id, 5)
    top_n_items = set(top_n['Item'])

    items_recommended = items_recommended | top_n_items

  return float(len(items_recommended))/float(len(items))


def user_coverage(users):
  users_covered = 0.0

  for user_id in users:
    top_n = get_top_n(user_id, 5).dropna()
    top_n_items = set(top_n['Item'])

    if top_n_items:
      users_covered += 1.0

  return users_covered/float(len(users))


def category_coverage(users, items):
  all_categories = set(map(lambda x: x['LeafCat'], items))
  covered_categories = set()

  for user_id in users:
    top_n = get_top_n(user_id, 5)

    top_n_categories = set()

    for item_id in top_n['Item']:
      item = get_item_by_id(item_id)
      top_n_categories = top_n_categories | set([item['LeafCat']])

    covered_categories = covered_categories | set(top_n_categories)

  return float(len(covered_categories))/float(len(all_categories))
