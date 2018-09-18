from data import get_relevant_items_for_user, get_top_n

def mrr(users):
  mrr = 0.0

  for user_id in users:
    user_relevant_items = get_relevant_items_for_user(user_id)
    top_n = get_top_n(user_id, 5)

    rank = 1.0

    for recommendation in top_n.iterrows():
      if recommendation[1]['Item'] in list(user_relevant_items['item']):
        mrr += 1.0/float(rank)

      rank += 1.0

  return  mrr/float(len(users))
