
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import psycopg2

app = Flask(__name__)

db = SQLAlchemy()


class Restaurant(db.Model):
    """Restaurant info."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer,
                                    primary_key=True,
                                    autoincrement=True)
    external_places_id = db.Column(db.String(30), nullable=False, unique=True)
    places_general_score = db.Column(db.Float, nullable=False, unique=False)
    name = db.Column(db.String(30), nullable=False, unique=True)
    internal_places_id = db.Column(db.String(50), nullable=False, unique=True)
    # places_reviews = db.column(db.String(300???))
    address = db.Column(db.String(100), nullable=False, unique=True)
    # open_hours = db.column(db.string(300???))
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.rating_id'))

    rating = db.relationship('Rating')


    def __repr__(self):
        """Show information about restaurant."""

        return "<Restaurant restaurant_id=%s name=%s  score=%s>" % (
            self.restaurant_id, self.name, self.places_general_score)


class User(db.Model):
    """User info."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                                    primary_key=True,
                                    autoincrement=True)
    fname = db.Column(db.String(15), nullable=False, unique=False)
    lname = db.Column(db.String(15), nullable=False, unique=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False, unique=True)
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.rating_id'))

    rating = db.relationship('Rating')

    def __repr__(self):
        """Show information about user."""

        return "<User fname=%s lname=%s  email=%s>" % (
            self.fname, self.lname, self.email)


class Rating(db.Model):
    """Rating info."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                                    primary_key=True,
                                    autoincrement=True)
    rating = db.Column(db.Integer, nullable=False, unique=False)
    review = db.Column(db.String(300), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))


    restaurant = db.relationship('Restaurant')
    user = db.relationship('User')

    def __repr__(self):
        """Show information about rating."""

        return "<Rating rating_id=%s" % (self.rating_id)

#******************************
#Helper functions

def connect_to_db(app):
    """Connect tthe database to the Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dininghero' # I will call this database dininghero
    app.config['SQLALCHEMY_ECHO'] = True # this line will print in the in the terminal
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



if __name__ == '__main__':
    app.debug = True
    from server import app #I do need to import app for this to run
    connect_to_db(app)
    print "Connected to DB."
