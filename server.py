import os
from flask import Flask, request, render_template, redirect, session, flash
from jinja2 import StrictUndefined
#from flask_debugtoolbar import DebugToolbarExtension
from twilio.rest import Client
from model import User, Rating, Restaurant, Day, Hour, Category, connect_to_db, db
app = Flask(__name__)
app.secret_key = "ABC" # you always need to give your app a secret key. No matter what key it is
# if you use an undefined variable in Jinja2, it fails
# silently. Adding this line raises an error instead.
app.jinja_env.undefined = StrictUndefined
import rollbar
rollbar_token = os.environ['ROLLBAR_POST_SERVER_ITEM_ACCESS_TOKEN']
rollbar.init(rollbar_token, 'production') 

@app.route('/')

def main_page(): 
    """Homepage"""

    return render_template('main_page.html')

@app.route('/vendors_registration')
def vendors_registration_information():
    """Renders information to vendors about site registration"""

    return render_template('vendors_registration.html')


@app.route('/vendors')
def vendors_page():
    """Renders information to vendors"""

    return render_template('vendors.html')


@app.route('/sms', methods=['POST'])
def send_sms():
    """Allows admin and vendor to send promo sms."""

    message = request.form.get('message')
    
    try:
        email = session['email']
    except KeyError:
        rollbar.report_exc_info()
        flash("You need to login to send a promo sms.")
        return redirect('/')

    user = User.query.filter_by(email=email).first()
    user_type = user.user_type

    if user_type == 'admin' or user_type == 'vendor':
    
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']

        client = Client(account_sid, auth_token)

        client.messages.create(
        to=os.environ['MY_PHONE_NUMBER'], #substitute by list of users when updated from trial Twilio acc
        from_=os.environ['MY_TWILIO_PHONE_NUMBER'],
        body=message
        )

        return render_template('message_sent.html', message=message)

    else:
        rollbar.report_message('You dont have authorization to send promo sms', 'warning')
        flash("You don't have authorization to send promo sms. If you are an admin or a vendor please contact us to request autorization.")
        return redirect('/')


@app.route('/restaurants')
def list_of_restaurants():
    """Show list of restaurants."""

    restaurants = Restaurant.query.order_by('name').all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/<rest_id>')
def restaurant_details(rest_id):
    """Shows each restaurant details."""

    restaurant = Restaurant.query.get(rest_id)

    return render_template('restaurant_details.html', restaurant=restaurant)


@app.route('/advanced_search_form')
def shows_user_form():
    """Allows user to perform advanced search"""

    return render_template('advanced_search.html')


@app.route('/advanced_search')
def user_form():
    """Allows user to perform advanced search"""

    desired_location = request.args.get('chosen_location')


      
    simple = request.args.get('sophistication')
    traditional = request.args.get('traditional') # no traditional/fusion added to current database
    brunch = request.args.get('brunch')
    outside = request.args.get('outside') # no outside added to current database
    tablecloth = request.args.get('tablecloth')
    ambience = request.args.get('ambience') # no ambience/decoration added to current database
    
    list_food_categories = []
   
    list_food_simple = db.session.query(Category).filter_by(specialty=simple).all()
    list_food_categories.extend(list_food_simple)
    list_food_brunch = db.session.query(Category).filter_by(specialty=brunch).all()
    list_food_categories.extend(list_food_brunch)
    list_food_outside = db.session.query(Category).filter_by(specialty=outside).all()
    list_food_categories.extend(list_food_outside)
    list_food_tablecloth = db.session.query(Category).filter_by(specialty=tablecloth).all()
    list_food_categories.extend(list_food_tablecloth)
    list_food_ambience = db.session.query(Category).filter_by(specialty=ambience).all()
    list_food_categories.extend(list_food_ambience)
    list_food_traditional = db.session.query(Category).filter_by(specialty=traditional).all()
    list_food_categories.extend(list_food_traditional) 
  

    if list_food_categories:
        print ('beginning of list of foods')
        print (list_food_categories)
        print ('end list of food')
        restaurants = []
        for category in list_food_categories:
            rest_id = category.restaurant_id
            restaurants.append(Restaurant.query.get(rest_id)) # appends the id of the rest


        return render_template('advanced_results.html', restaurants=restaurants)

    else:
        flash("Oops! Couldn't find that. Please try something else!")
        return redirect('/')
    
        # either change /results to advanced_results or make sure the results refresh
        # return render_template('advanced_results.html') # need to create thi html

@app.route('/show-login', methods=['GET'])
def show_login():
    """Gives back the login form"""

    return render_template('login.html')


@app.route('/login')
def login_form():
    """Shows login form."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Alows user to login"""

    email = request.form.get('email')
    password = request.form.get("password")

    user = db.session.query(User).filter_by(email=email).first()


    if user and password == user.password:

        session['email'] = email
        session['user_type'] = user.user_type
        flash('Login sucessful!')

        return redirect('/profile')
    else:
        rollbar.report_message('Login failed', 'warning')
        flash('Login failed. We could not find your email or password.')
        return redirect('/login')


@app.route('/registration')
def registration_form():
    """show registration form"""

    return render_template("registration_form.html")


@app.route('/registration', methods=['POST'])
def confirm_registration():
    """Confirms registration"""

    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    username = request.form.get('username')
    phone = request.form.get('phone')

    if not email or not password or not fname or not username or not phone:
        rollbar.report_message('All fields are required!', 'warning')
        flash('All fields are required!')
        return redirect('/registration')

    duplicates = db.session.query(User).filter_by(email=email).all()

    if duplicates:
        flash('This email is already registered. Please try again with a different email.')
        return redirect('/registration')
    else:
        new_user = User(email=email, password=password, fname=fname, username=username, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        flash('You have been registered!')
        session['email'] = email

    return redirect('/profile') 


@app.route('/profile')
def show_profile():
    """show user profile"""
    try:
        email = session['email']

        user = User.query.filter_by(email=email).first()
      
        rated_restaurants = user.rating #this is a list

        favorite_spots = []

        for rating in rated_restaurants:
            if rating.score == 5:
                if len(favorite_spots) < 6:
                    favorite_spots.append(rating.restaurant)

        return render_template('profile.html', favorite_spots=favorite_spots)

    except KeyError:
        rollbar.report_exc_info()
        flash('You need to login in to see your profile!')
        return redirect('/show-login')
        

@app.route('/results')
def results():
    """shows users restaurant suggestion"""
    
    food_type = request.args.get('type_of_food')
    food_type = food_type.title()

    list_food_categories = db.session.query(Category).filter_by(specialty=food_type).all()

    if list_food_categories:
        restaurants = []
        for category in list_food_categories:
            rest_id = category.restaurant_id
            restaurants.append(Restaurant.query.get(rest_id))

        return render_template('results.html', restaurants=restaurants)

    else:
        flash("Oops! Couldn't find that. Please try something else!")
        return redirect('/')


@app.route('/rating', methods=['POST'])
def rate_a_restaurant():
    """Rating for a restaurant"""

    restaurant_id = request.form.get('restaurant')
    user_review = request.form.get('user_review')
    score = request.form.get('score')
    restaurant = Restaurant.query.get(restaurant_id)

    try:
        email = session['email']

        user = User.query.filter_by(email=email).first()
        user_id = user.user_id
        rating = Rating.query.filter(Rating.user_id == user_id, Rating.restaurant_id == restaurant_id).first()
        if rating:
            rating.score = score
            db.session.commit()
            flash('You changed the rating for ' + restaurant.name + ' . The new score is ' + score + '.')
            return redirect('/rating_results')

        else:
        
            new_rating = Rating(restaurant_id=restaurant_id, user_id=user_id, score=score, user_review=user_review)
            db.session.add(new_rating)
            db.session.commit()
            flash('You gave ' + score + ' stars to ' + restaurant.name)
            return redirect('/rating_results')

    except KeyError:
        rollbar.report_exc_info()
        flash('You need to login in order to add a rating!')
        return redirect('/')


@app.route('/rating_results')
def rating_results():
    """Show rating results"""

    restaurants = Restaurant.query.order_by('name').all()
    return render_template("rating_results.html", restaurants=restaurants)


@app.route('/rated')
def show_favorite_restaurants():
    """Show favorite restaurants"""

    restaurants = Restaurant.query.order_by('restaurant_id').all()
    for restaurant in restaurants:
        restaurant_id = restaurant.restaurant_id

    email = session['email']

    user = User.query.filter_by(email=email).first()
  
    rated_restaurants = user.rating #this is a list

    return render_template('rated_restaurants.html', rated_restaurants=rated_restaurants)


@app.route('/favorite_spots')
def show_restaurants_rated_five():
    """show user profile"""
    try:
        email = session['email']

        user = User.query.filter_by(email=email).first()
      
        rated_restaurants = user.rating #this is a list

        favorite_spots = []

        for rating in rated_restaurants:
            if rating.score == 5:
                if len(favorite_spots) < 6:
                    favorite_spots.append(rating.restaurant)

        return render_template('favorite_spots.html', favorite_spots=favorite_spots)

    except KeyError:
        rollbar.report_exc_info()
        flash('You need to be logged in to see your favorite spots!')
        return redirect('/show-login')


@app.route('/logout')
def log_out():
    """Logs the user out"""

    del session['email']
    session.clear()
    flash('You are logged out!')

    return redirect('/')


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    
    app.run() # the app.run should be the last thing on your app in order to not cause conflicts
