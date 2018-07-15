
from data import get_top_n, is_item_relevant_for_user, is_item_popular

def serendipity(users):
    serendipity = 0.0

    for user_id in users:
        top_n = get_top_n(user_id, 5)
        top_n_items = set(top_n['Item'])

        top_n_serendipity = 0.0

        for item_id in top_n_items:
            if is_item_relevant_for_user(user_id, item_id) and not is_item_popular(item_id):
                top_n_serendipity += 1.0

        serendipity += top_n_serendipity/float(len(top_n_items))

    return serendipity/float(len(users))