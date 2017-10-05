from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()


class Restaurant(db.Model):
    """Restaurant info."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer,
                                    primary_key=True,
                                    autoincrement=True)
    external_places_id = db.Column(db.String(30), nullable=False, unique=True)
    general_score = db.Column(db.Float, nullable=False, unique=False)
    name = db.Column(db.String(30), nullable=False, unique=True)
    internal_places_id = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False, unique=True)
    

    rating = db.relationship('Rating')
    hour = db.relationship('Hour')


    def __repr__(self):
        """Show information about restaurant."""

        return "<Restaurant restaurant_id=%s name=%s  score=%s>" % (
            self.restaurant_id, self.name, self.general_score)


class User(db.Model):
    """User info."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    fname = db.Column(db.String(15), nullable=False, unique=False)
    lname = db.Column(db.String(15), nullable=True, unique=False)
    email = db.Column(db.String(20), nullable=False, unique=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False, unique=True)

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
    score = db.Column(db.Integer, nullable=False, unique=False)
    user_review = db.Column(db.Text, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=True)


    restaurant = db.relationship('Restaurant')
    user = db.relationship('User')

    def __repr__(self):
        """Show information about rating."""

        return "<Rating rating_id=%s score=%s user_review=%s" % (self.rating_id,
            self.score, self.user_review)

class Hour(db.Model):
    """Open_hours info."""

    __tablename__ = "hours"

    hour_id = db.Column(db.Integer,
                                    primary_key=True,
                                    autoincrement=True)
    open_time = db.Column(db.String(20), nullable=False, unique=False)
    closing_time = db.Column(db.String(20), nullable=True, unique=False)
    additional_hours = db.Column(db.String(15), nullable=True, unique=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=True)
    day_id = db.Column(db.String(10), db.ForeignKey('days.day'), nullable=True)

    restaurant = db.relationship('Restaurant')
    day = db.relationship('Day')

    def __repr__(self):
        """Show information about open_hours."""

        return "<Hour open_time=%s closing_time=%s day=%s" % (self.open_time, self.closing_time, self.day)


class Day(db.Model):
    """Open_days info."""

    __tablename__ = "days"


    day = db.Column(db.String(10), primary_key=True, nullable=False, unique=False)
    

    hour = db.relationship('Hour')

    def __repr__(self):
        """Show information about open_days."""

        return "<Day day=%s" % (self.day)


#******************************
#Helper functions

def connect_to_db(app):
    """Connect tthe database to the Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dininghero' # I will call this database dininghero
    app.config['SQLALCHEMY_ECHO'] = True # this line will print in the in the terminal
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # this avoids silly error message from track modifications
    db.app = app
    db.init_app(app)



if __name__ == '__main__':
    app.debug = True
    from server import app #I do need to import app for this to run
    connect_to_db(app)
    print "Connected to DB."
