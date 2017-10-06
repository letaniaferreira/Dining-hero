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
def main_page():
    """Homepage"""

    return render_template('main_page.html')

@app.route('/search')
def quick_search():
    """Allows user to do basic search"""
   
    food_type = request.args.get('type_of_food')

    food_category = db.session.query(Category).filter_by(specialty=food_type).all()
   
    if food_category:
        return render_template('results.html')

    else:
        flash("Ops! Couldn't find that. Please try something else!")
        return redirect('/')


@app.route('/advanced_search')
def user_form():
    """Allows user to perform advanced search"""

    desired_location = request.args.get('chosen_location')

    if desired_location == "haight":
        print "I work"

    # add other request forms here

    #verify return route - why is it going back to main_page?

    return render_template('advanced_search.html')

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

    return render_template('results.html')

if __name__ == "__main__":

    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    
    app.run(debug=True) # the app.run should be the last thing on your app in order to not cause conflicts
