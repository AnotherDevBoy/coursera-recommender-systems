from data import get_top_n

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
        top_n = get_top_n(user_id, 5)
        top_n_items = set(top_n['Item'])

        if top_n_items:
            users_covered += 1.0

    return users_covered/float(len(users))