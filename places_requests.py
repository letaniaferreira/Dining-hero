import requests
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
        author_name = review['author_name']
        made_up_pass = review['time']
        reviews_dictionary[review['rating']].extend([author_name, made_up_pass, review['text']])
    place_address = restaurant_info['result'].get('formatted_address')
    place_general_hours = restaurant_info['result'].get('opening_hours')
    place_hours = place_general_hours['weekday_text']
    for day in place_hours:
        Monday = place_hours[0]
        Tuesday = place_hours[1]
        Wednesday = place_hours[2]
        Thursday = place_hours[3]
        Friday = place_hours[4]



    print "general_score: {}".format(place_general_score)
    print "rest_name:{}".format(place_name)
    print "internal_id: {}".format(place_num_id)
    print "reviews: {}".format(reviews_dictionary)
    print "adress:{}".format(place_address)
    print "open_hours:{}".format(place_hours)
    print Monday
    print Tuesday

request_data_from_google_places('ChIJMZnCJCJ-j4ARN5S_0ANESiM')
request_data_from_google_places('ChIJlx0LN6-AhYARRNIyIbXTAWY')

