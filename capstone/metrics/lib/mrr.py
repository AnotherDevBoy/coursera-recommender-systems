

def mrr_for_user(top_n, user_relevant_items):
  mrr = 0.0
  rank = 1.0

  for recommendation in top_n.iterrows():
    if recommendation[1]['Item'] in list(user_relevant_items['Item']):
      mrr += 1.0/float(rank)

    rank += 1.0

  return mrr
