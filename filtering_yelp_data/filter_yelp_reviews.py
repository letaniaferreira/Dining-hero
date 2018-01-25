import json
import csv
import string
import os

def get_all_reviews_for_restaurant(dict):
    """gets reviews from json returns reviews dictionary"""

    reviews_dict = {}
    

    for row in open('review.json'):
        row = row.rstrip()
        row = json.loads(row)

        
        review = row['text']
        business_id = row['business_id']

        restaurant_info = dict.get(business_id)

        if restaurant_info is not None:

            if business_id not in reviews_dict:

                reviews_dict[business_id] = [review]  

            else:

                reviews_dict[business_id] += [review]       


    return reviews_dict

def read_restaurants(file):
    """reads restaurants file"""
    with open(file, 'r') as file:
            data = file.read()
            data = json.loads(data)
            
                    
    return data

def write_results_to_file(file, reviews):
    """Writes result to file"""

    counter = 1
    max_file_size = 50

    type_of_food = ['Pizza', 'Pub', 'Fench', 'Thai', 'Brunch', 'Soul', 'Italian', 'Vegetarian', 'Chinese', 'Seafood', 'Mexican', 'Indian', 'Vegan', 'Sandwiches', 'Japanese', 'Burguers', 'Fast Food', 'Salad', 'Desserts', 'Bar', 'Barbeque']

    for key, value in restaurants_dict.items():

        first_category = get_first_non_restaurant_categories(value[1])
        if first_category in type_of_food:

            with open(get_file_name(file, counter), 'a') as csvfile:
                data_writer = csv.writer(csvfile, delimiter=',')
                                    # quotechar='"', quoting=csv.QUOTE_MINIMAL)

                if key in reviews:
                    reviews_list = reviews[key]
                    commaless_list = clean_strings(reviews_list)
                    for item in commaless_list:


                        data_writer.writerow(join_strings(item, first_category))

                if os.path.getsize(csvfile.name) / 1000000 > max_file_size:
                    counter +=1


def get_file_name(file_name, counter):
    """ gets a string file name
        >>> get_file_name("test", 1)
        'test.1.csv'
    """
    return "{}.{}.csv".format(file_name, counter)


def get_first_non_restaurant_categories(categories_lst):
    """ gets first restaurant category if value is not "Restaurants"
        >>> get_first_non_restaurant_categories([])
        >>> get_first_non_restaurant_categories(["Restaurants", "Chinese"])
        'Chinese'
        >>> get_first_non_restaurant_categories(["Italian", "Pasta"])
        'Italian'
    """

    if categories_lst == []:
        return None

    if categories_lst[0] == "Restaurants" and len(categories_lst) >= 2:
        return categories_lst[1]

    else:
        return categories_lst[0]

def join_strings(commaless_lst, category_str):
    """ joins food category and commaless reviews
        >>> join_strings(['test', 'one two three'], "Chinese")
        ['test one two three', 'Chinese']
    """
    return [" ".join(commaless_lst), category_str]


def clean_strings(lst):
    """ Removes commas from all strings in the list
        >>> clean_strings(["one, two, three"])
        ['one two three']
        >>> clean_strings(["test", "one, two, three"])
        ['test', 'one two three']
        >>> clean_strings(["test", "one, two, and three\xc5\xbe"])
        ['test', 'one two and three']
        >>> clean_strings(["test", "one, two, three.\\n Next line."])
        ['test', 'one two three. Next line.']
    """
    commaless_list = [] 
    for item in lst:
        printable = set(string.printable)
        review = filter(lambda x: x in printable, item)
        clean_review = review.replace("\n", "")
        commaless_list.append(clean_review.replace(",", ""))
    return commaless_list


print "Reading restaurants..."
restaurants_dict = read_restaurants('yelp_dict_rest_json.txt')
print "Getting reviews for restaurants..."
reviews = get_all_reviews_for_restaurant(restaurants_dict)
print "Opa!!! Writing to the file..."
rest_file = write_results_to_file('results/classified_reviews', reviews)


