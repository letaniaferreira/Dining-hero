import json


def separate_restaurant():
    """makes dictionary of restaurants using name and category"""

    dict_of_restaurant_ids = {}

    for row in open('business.json'):
        row = row.rstrip()
        row = json.loads(row)
        categories_list = row['categories']
        restaurant_id = row['business_id']
        restaurant_name = row['name']

        if "Restaurants" in categories_list:
            dict_of_restaurant_ids[restaurant_id] = [restaurant_name, categories_list]

    return dict_of_restaurant_ids


def write_results_to_file(file):
    """Writes requests result to file."""

    with open(file, 'w') as file:
        file.write(json.dumps(yelp_rest_info))


yelp_rest_info = separate_restaurant()
write_results_to_file('yelp_dict_rest_json.txt')
