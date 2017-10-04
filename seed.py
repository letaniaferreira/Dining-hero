# from sqlalchemy import func
# from model import User
# from model import Rating
# from model import Restaurant
# from model import connect_to_db, db
# from server import app
import ast

# def load_restaurants():
#     """Load restaurants from file into database."""

#     print "Restaurants"

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Restaurant.query.delete()

#     for row in open("data_3_restaurants.txt"):
#         # if not row.startswith('#') and not row.strip() == "":
#         row = row.rstrip().split("|")
        
#         external_places_id = row[0]
#         general_score = row[1]
#         name = row[2]
#         internal_places_id = row[3]
#         address = row[5]


#         restaurant = Restaurant(external_places_id=external_places_id,
#                                 general_score=general_score,
#                                 name=name,
#                                 internal_places_id=internal_places_id,
#                                 address=address)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(restaurant)

#     # Once we're done, we should commit our work
#     db.session.commit()

# def load_users():
#     """Load users from file into database."""

#     print "Users"

#     User.query.delete()

#     for row in open("data_3_restaurants.txt"):
#         if not row.startswith('#') and not row.strip() == "":
#             row = row.rstrip().split("|")
#             reviews = row[4]
#             reviews_dictionary = ast.literal_eval(reviews) #serialization - converting types to raw format
#             for key, value in reviews_dictionary.items():
#                 if reviews_dictionary[key] != []:
#                     user_information = reviews_dictionary[key]
#                     for user_info in user_information:
#                         user_id = user_info['user_id']
#                         password = user_info['password']
#                         full_name = user_info['name']
#                         for name in full_name:
#                             fname, second_name = full_name.split(" ")
#                             lname = second_name[0]
#                             username = fname + lname
#                             email = fname + "@gmail.com"


#                         user = User(fname=fname,
#                                     lname=lname,
#                                     email=email,
#                                     username=username,
#                                     password=password,
#                                     user_id=user_id)

#                         db.session.add(user)
#     db.session.commit()    

# def load_ratings():
#     """Load ratings from file into database."""

#     print "Ratings"

#     Rating.query.delete()

#     for row in open("data_3_restaurants.txt"):
#         if not row.startswith('#') and not row.strip() == "":
#             row = row.rstrip().split("|")
#             reviews = row[4]
#             reviews_dictionary = ast.literal_eval(reviews) 
#             for key, value in reviews_dictionary.items():
#                 if reviews_dictionary[key] != []:
#                     user_information = reviews_dictionary[key]
#                     score = key
#                     for user_info in user_information:
#                         user_review = user_info['user_review']

#                         rating = Rating(user_review=user_review,
#                                         score=score)

#                         db.session.add(rating)
#     db.session.commit()

# def load_days():
#     """Load restaurants from file into database."""

#     print "Days"

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Day.query.delete()

    for row in open("data_3_restaurants.txt"):
        # if not row.startswith('#') and not row.strip() == "":
        row = row.rstrip().split("|")
        
        day_and_time = row[6]
        print day_and_time[0]
        

#         day = Day(day=day)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(day)

#     # Once we're done, we should commit our work
#     db.session.commit()


# if __name__=='__main__':
#     connect_to_db(app)

#     #if table have not been created, create them
#     db.create_all()

#     #calling the functions
#     load_restaurants()
#     load_users()
#     load_ratings()
#     load_days()