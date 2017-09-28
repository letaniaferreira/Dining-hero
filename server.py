from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def main_page():
    """Allows user to do basic search"""

    food_type = request.args.get('type_of_food')

    return render_template('main_page.html')

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


@app.route('/login', methods=['Post'])
def login():
    """Alows user to login"""

    username = request.form['username']
    password = request.form['password']

    # session['username'] = password
    return render_template('login.html')

@app.route('/results')
def results():
    """shows users restaurant suggestion"""

    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=True)