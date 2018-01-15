import requests
import os
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def request_data_from_google_places(place_id):
    """Takes a place_id from googleplaces and returns information about business"""

    google_places_key=os.environ['PLACES_API_KEY']

    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(place_id, google_places_key)

    results = requests.get(url)

    restaurant_info = results.json()

    place_num_id = restaurant_info['result'].get('id')

    place_name = restaurant_info['result'].get('name')

    place_general_score = restaurant_info['result'].get('rating')

    reviews_dictionary = {1:[], 2:[], 3:[], 4:[], 5:[]}
    reviews = restaurant_info['result'].get('reviews')
    for review in reviews:
        author_name = review['author_name']
        made_up_pass = review['time']
        text_review = review['text']
        reviews_dictionary[review['rating']].append({'user_id':'!!!user_id!!!!', 'name':author_name, 'password':made_up_pass, 'user_review':text_review, 'user_type': '!!!!usertype!!!!'})

    place_address = restaurant_info['result'].get('formatted_address')

    restaurant_id = '!!!!rest_id!!!'

    place_general_hours = restaurant_info['result'].get('opening_hours', None)

    if place_general_hours != None:
        place_hours = place_general_hours['weekday_text']
    else:
        place_hours = None

    return [place_id, restaurant_id, place_general_score, place_name, place_num_id, reviews_dictionary, place_address, place_hours]

general_results = request_data_from_google_places('ChIJiwOc1iJ-j4ARmtSY2tM29G0')


def save_requests_results():
    """Saves requests results."""

    places_id_list = ['ChIJNTBFxKyAhYARXPtpITIjvIQ', 'ChIJx1ULhNCAhYARSRq9NDWTeqI'] #, 'ChIJxSa9TqKAhYAR4lqep-kTo8c', 'ChIJMZnCJCJ-j4ARN5S_0ANESiM', 'ChIJiwOc1iJ-j4ARmtSY2tM29G0', 'ChIJVVWVjGaAhYARH_4JjCTVBz8', 'ChIJYykKebmAhYAR0f6JEcUdIVs', 'ChIJU8wGk6aAhYARW4WqEGx2HNE', 'ChIJqzfjw6aAhYARyCQ9qVcoIU0', 'ChIJ30-kn0F-j4ARM4P0RtSVENA']

    list_of_API_results = []

    for places_id in places_id_list:
        list_of_API_results.append(request_data_from_google_places(places_id))

    return json.dumps(list_of_API_results)

data_10_restaurants = save_requests_results()


def write_results_to_file(file):
    """Writes requests result to file."""

    with open(file, 'w') as file:
        file.write(data_10_restaurants)

rest_file = write_results_to_file('data_10_rest_json.txt')


