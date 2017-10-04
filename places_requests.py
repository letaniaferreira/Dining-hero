import requests
import os
import sys
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
        reviews_dictionary[review['rating']].append({'name':author_name, 'password':made_up_pass, 'user_review':text_review})

    place_address = restaurant_info['result'].get('formatted_address')

    place_general_hours = restaurant_info['result'].get('opening_hours')

    place_hours = place_general_hours['weekday_text']
    

    return [place_id, place_general_score, place_name, place_num_id, reviews_dictionary, place_address, place_hours]

general_results = request_data_from_google_places('ChIJiwOc1iJ-j4ARmtSY2tM29G0')







