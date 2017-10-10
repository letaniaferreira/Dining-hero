from flask import Flask, request, render_template, redirect, session, flash

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Restaurant, Day, Hour, Category, connect_to_db, db

app = Flask(__name__)

app.secret_key = "ABC" # you always need to give your app a secrete key. No matter what key it is 

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
#need this showing page to not get conflict with the get form
def main_page(): 
    """Homepage"""

    return render_template('main_page.html')


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
        restaurants = []
        for category in list_food_categories:
            rest_id = category.restaurant_id
            restaurants.append(Restaurant.query.get(rest_id)) # appends the id of the rest


        return render_template('advanced_results.html', restaurants=restaurants)

    else:
        flash("Ops! Couldn't find that. Please try something else!")
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


@app.route('/login', methods=['Post'])
def login():
    """Alows user to login"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(User).filter_by(email=email).first()


    if user and password == user.password:

        session['email'] = email
        flash("Login sucessful!")
        return render_template('advanced_search.html')
    else:
        flash("Login failed. Incorrect email or password.")
        return redirect('/login')


@app.route('/results')
def results():
    """shows users restaurant suggestion"""
    
    food_type = request.args.get('type_of_food')

    
    list_food_categories = db.session.query(Category).filter_by(specialty=food_type).all()

    if list_food_categories:
        restaurants = []
        for category in list_food_categories:
            rest_id = category.restaurant_id
            restaurants.append(Restaurant.query.get(rest_id))


        return render_template('results.html', restaurants=restaurants)

    else:
        flash("Ops! Couldn't find that. Please try something else!")
        return redirect('/')

if __name__ == "__main__":

    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    
    app.run(debug=True) # the app.run should be the last thing on your app in order to not cause conflicts
