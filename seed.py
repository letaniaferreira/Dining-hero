
from sqlalchemy import func
from model import User
from model import Rating
from model import Restaurant

from model import connect_to_db, db
from server import app

def load_restaurants():
    """Load users from u.user into database."""

    print "Restaurants"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Restaurant.query.delete()

    # Read u.user file and insert data
    for row in open("data_10_restaurants.txt"):
        # if not row.startswith('#') and not row.strip() == "":
        row = row.rstrip().split("|")
        
        external_places_id = row[0]
        score = row[1]
        name = row[2]
        internal_id = row[3]
        address = row[5]

        print external_places_id

        restaurant = Restaurant(name=name,
                    score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(restaurant)

    # Once we're done, we should commit our work
    db.session.commit()

def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("data_10_restaurants.txt"):
        row = row.rstrip().split("|")
        
        # external_places_id = row[0]
        # score = row[1]
        # name = row[2]
        # internal_id = row[3]
        # address = row[5]

        # print external_places_id

        # user = User(name=name,
        #             score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()    

if __name__=='__main__':
    connect_to_db(app)

    #if table have not been created, create them
    db.create_all()

    #calling the functions
    load_restaurants()
    load_users()