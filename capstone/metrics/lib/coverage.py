from data import get_item_field_by_id


def is_user_covered(top_n):
  return len(set(top_n['Item']))


def category_coverage_for_user(top_n):
  top_n_categories = set()

  for item_id in top_n['Item']:
    top_n_categories = top_n_categories | set([get_item_field_by_id(item_id, 'LeafCat')])

  return set(top_n_categories)
