import requests
import os

def request_data_from_google_places(place_id):
    """Takes a place_id from googleplaces and returns information about business"""

    google_places_key=os.environ['PLACES_API_KEY']

    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(place_id, google_places_key)

    r = requests.get(url)
    # r.status_code
    # r.headers['content-type']
    # r.encoding
    # r.text
    restaurant_info = r.json()

    place_num_id = restaurant_info['result'].get('id')
    place_name = restaurant_info['result'].get('name')
    place_general_score = restaurant_info['result'].get('rating')
    reviews_dictionary = {1:[], 2:[], 3:[], 4:[], 5:[]}
    reviews = restaurant_info['result'].get('reviews')
    for review in reviews:
        reviews_dictionary[review['rating']].append(review['text'])
    place_address = restaurant_info['result'].get('formatted_address')
    place_general_hours = restaurant_info['result'].get('opening_hours')
    place_hours = place_general_hours['weekday_text']



    print "general score: {}".format(place_general_score)
    print "Name:{}".format(place_name)
    print "Number_id: {}".format(place_num_id)
    print "Reviews: {}".format(reviews_dictionary)
    print "Location:{}".format(place_address)
    print "Open hours:{}".format(place_hours)

request_data_from_google_places('ChIJMZnCJCJ-j4ARN5S_0ANESiM')

