from sqlalchemy import func
from model import User
from model import Rating
from model import Restaurant
from model import Category
from model import Day
from model import Hour
from model import connect_to_db, db
from server import app
import json

from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"

def open_file(file):

    with open(file, 'r') as file:
        data = file.read()
        data = json.loads(data)

    return data

def load_restaurants(data):
    """Load restaurants from file into database."""

    print "Restaurants"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Restaurant.query.delete()

    for restaurant_info in data:
        external_places_id = restaurant_info[0]
        restaurant_id = restaurant_info[1]
        general_score = restaurant_info[2]
        name = restaurant_info[3]
        internal_places_id = restaurant_info[4]
        address = restaurant_info[6]

        restaurant = Restaurant(external_places_id=external_places_id,
                                general_score=general_score,
                                name=name,
                                internal_places_id=internal_places_id,
                                address=address,
                                restaurant_id=restaurant_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(restaurant)

        # Once we're done, we should commit our work
        db.session.commit()


def load_categories(data):
    """Load categories from file into database."""

    print "Categories"

    Category.query.delete()

    for restaurant_info in data:
        restaurant_id = restaurant_info[1]
        special_features = restaurant_info[8]
        for special in special_features:
#there is repetition in the categories as of right now, but categories have been added

            category = Category(specialty=special,
                                restaurant_id=restaurant_id)

            db.session.add(category) 

        db.session.commit()


def load_users(data):
    """Load users from file into database."""

    print "Users"

    User.query.delete()

    for restaurant_info in data:
        reviews_dictionary = restaurant_info[5]
        for key, value in reviews_dictionary.items():
            if reviews_dictionary[key] != []:
                user_information = reviews_dictionary[key]
                for user_info in user_information:
                    user_id = user_info['user_id']
                    password = user_info['password']
                    full_name = user_info['name']
                    for name in full_name:
                        fname = full_name[:5]
                        lname = full_name[0]
                        username = fname + str(password)
                        email = fname + "@gmail.com"

                    user = User(user_id=user_id,
                                fname=fname,
                                lname=lname,
                                email=email,
                                username=username,
                                password=password)

                    db.session.add(user)

    db.session.commit()    

def load_ratings(data):
    """Load ratings from data file into database."""

    print "Ratings"

    Rating.query.delete()

    for restaurant_info in data:
        restaurant_id = restaurant_info[1]
        reviews_dictionary = restaurant_info[5] 
        for key, value in reviews_dictionary.items():
            if reviews_dictionary[key] != []:
                user_information = reviews_dictionary[key]
                score = key
                for user_info in user_information:
                    user_review = user_info['user_review']
                    user_id = user_info['user_id']
                    
                    rating = Rating(score=score,
                                    user_review=user_review,
                                    user_id=user_id,
                                    restaurant_id=restaurant_id)

                    db.session.add(rating)

    db.session.commit()

def load_days(data):
    """Load days data into database."""

    print "Days"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Day.query.delete()

    days = [("Mo","Monday"), ("Tu", "Tuesday"), ("We", "Wednesday"),
     ("Th", "Thursday"), ("Fr", "Friday"), ("Sa", "Saturday"), ("Su", "Sunday")]
    for week_day in days:
        day = week_day[1]
        day = Day(day=day)

        db.session.add(day)

    db.session.commit()

def load_hours(data):
    """Load hours data into database."""

    print "Hours"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Hour.query.delete()

    for restaurant_info in data:
        restaurant_id = restaurant_info[1]
        day_and_time = restaurant_info[7]
        if day_and_time != None:
            for day in day_and_time:
                days = day.split(':')
                week_day = days[0]
                if len(days) > 2:
                    open_time = days[1] + ":" + days[2][:5]
                    closing_time = days[2][-2:] + ":" + days[3][:-3]


                    hour = Hour(open_time=open_time, 
                                closing_time=closing_time, 
                                restaurant_id=restaurant_id,
                                day_id=week_day)
        
                    db.session.add(hour)

                    if len(days) > 4:
                        open_time = days[3][-1:] + ":" + days[4] + ":" + days[5]

                        hour = Hour(open_time=open_time,
                            restaurant_id=restaurant_id,
                            day_id=week_day)

                        db.session.add(hour)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__=='__main__':
    connect_to_db(app)

    db.drop_all()
    #if table have not been created, create them
    db.create_all()

# # calling the functions
    data_file = open_file('data_10_rest_json.txt')
    load_restaurants(data_file)
    load_categories(data_file)
    load_users(data_file)
    load_ratings(data_file)
    load_days(data_file)
    load_hours(data_file)
    set_val_user_id()