import json

# Load the JSON file
with open('categories.json', 'r', encoding='utf-8') as file:
    categories = json.load(file)

# Extract the IDs
category_ids = [str(category['id']) for category in categories]

# Join the IDs with commas and print
print(','.join(category_ids))
