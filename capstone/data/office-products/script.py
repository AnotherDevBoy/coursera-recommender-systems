import json

items = []

with open('items.json') as fp:  
    line = fp.readline()
    while line:
        item = json.loads(line)
        items.append(item)
        line = fp.readline()

good_items = json.dumps(items)

with open('good_items.json', 'w') as good_items_file:
    good_items_file.write(good_items)
