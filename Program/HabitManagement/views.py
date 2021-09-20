# The views.py file contains all the routes and their functionality

from flask import Blueprint, render_template, request, flash, json, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from HabitManagement import globals as g
from .analytics import same_periodicity, longest_streak_all, longest_streak_task
from datetime import date
from os import path, listdir

# Defines that this file is a blueprint of the application
# Can store multiple URLs inside of it
views = Blueprint('views', __name__)

# The decorator defines a route
# The URL is defined and what methods the route allows


@views.route('/login', methods=['GET', 'POST'])
def login():
    """Manages the login page"""
    # Checks if the request was a POST method
    if request.method == 'POST':
        # Stores the user input of the form in variables
        username = request.form.get('username')
        password = request.form.get('password')

        # Checks if a .json file of the user exists, based on the username
        if path.isfile(f"./Data/{username}.json"):
            # The context manager stores the content of the .json file in user_json
            with open(f"Data/{username}.json", "r") as file:
                user_json = json.loads(file.read())

            # Stores the password of the .json file in json_password
            json_password = user_json['user_data'][0]['password']

            # Checks if the entered password and the stored password are the same
            # Checks hash value of both passwords with check_password_hash
            if check_password_hash(json_password, password):
                # Calls the load_data function, which stores the data in the habit object
                g.habit.load_data(username)

                # Flashes a success message to the user
                flash('Loged in successfully', category="success")

                # Redirects the user to the views.home route
                return redirect(url_for('views.home'))

            # If the password is not the same
            else:
                # Flashes a error message to the user
                flash('The password is wrong!', category="error")

        # If the username does not exist
        else:
            # Flashes a error message to the user
            flash('The username does not exist!', category="error")

    # Renders the html of login.html in the templates folder
    return render_template("login.html")


@views.route('/logout')
def logout():
    # Checks for the login status
    if g.habit.login_status == False:
        flash('Please login to access this page', category="error")
        return redirect(url_for('views.login'))
    else:
        """Handles the logout of a user"""
        # Sets the login status of a user to false (logged out)
        g.habit.login_status = False

        # Redirects the user to the views.login route
        return redirect(url_for('views.login'))


@views.route('/register', methods=['GET', 'POST'])
def register():
    """Manages the resgistration page"""
    # Checks if the request was a POST method
    if request.method == 'POST':
        # Stores the user input of the form in variables
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        def registration(email, username, password1):
            """The actual registration of the user"""
            # Creates a dictionary user_json, which stores the user_data dictionary and habit_data dictionary with empty lists
            user_json = {"user_data": [], "habit_data": []}
            # Creates a dictionary registration_data, which stores the user inputs
            # Stores the password encrypted, with generate_password_hash
            registration_data = {"email": email, "username": username,
                                 "password": generate_password_hash(password1, method='sha256')}
            # Appends registration_data to the user_json, user_data dictionary list
            user_json['user_data'].append(registration_data)
            # The data from user_json is then formatted with json.dumps and stored in jsonStr
            jsonStr = json.dumps(user_json, indent=4, sort_keys=False)

            # Context manager opens the .json file and stores writes the jsonStr inside the file
            with open(f"Data/{username}.json", "w") as file:
                file.write(jsonStr)

            # Sets the login status to true (logged in)
            g.habit.login_status = True
            # Loads the data from the .json file in the habit object
            g.habit.load_data(username)

        # Checks if the email is at least 3 characters
        if len(email) < 4:
            # Flashes an error message to the user
            flash('Email must be greater than 3 characters!', category="error")

        # Checks if the username is at least 1 character
        elif len(username) < 1:
            # Flashes an error message to the user
            flash('Username must be at least 1 character!', category="error")

        # Checks if the password and password confirmation are the same
        elif password1 != password2:
            # Flashes an error message to the user
            flash('The passwords do not match!', category="error")

        # Checks if the password is greater than 3 characters
        elif len(password1) < 4:
            # Flashes an error message to the user
            flash('The password must be greater than 3 characters!', category="error")

        # Checks if the username already exists
        elif path.isfile(f"./Data/{username}.json"):
            # Flashes an error message to the user
            flash('This username already exists!', category="error")

        # Checks if the directory of "Data" is not empty
        elif len(listdir('./Data')) != 0:
            # Iterates through all files in "Data" and stores the filenames in "filename"
            for filename in listdir('./Data'):
                # Context manager opens the file, reads the content from the file as and stores it as "text"
                with open(f"./Data/{filename}") as currentFile:
                    text = currentFile.read()
                    # Checks if the entered email is in "text"
                    if email in text:
                        # Flashes an error message to the user
                        flash('This email adress already exists!',
                              category="error")
                    # If email is not in text
                    else:
                        # Flashes a success message to the user
                        flash('Account created!', category="success")
                        # Calls the registration function and registers the user
                        registration(email, username, password1)
                        # Redirects the user the views.home route
                        return redirect(url_for('views.home'))

        # If the "Data" directory is empty, registration happens directly
        else:
            # Flashes a success message to the user
            flash('Account created!', category="success")
            # Calls the registration function and registers the user
            registration(email, username, password1)
            # Redirects the user the views.home route
            return redirect(url_for('views.home'))

    # Renders the html of register.html in the templates folder
    return render_template("register.html")


@views.route('/')
def home():
    """Manages the homepage"""
    # Renders the html of home.html in the templates folder and passes the login status to the html file
    return render_template("home.html", login_status=g.habit.login_status)


@views.route('/analytics', methods=['GET', 'POST'])
def analytics():
    """Manages the analytics page"""
    # Checks for the login status
    if g.habit.login_status == False:
        flash('Please login to access this page', category="error")
        return redirect(url_for('views.login'))
    else:
        # Calls longest_streak_all from analytics and assigns it
        list_longest_streak = longest_streak_all()

        # Creates empty lists as placeholders
        list_periodicity = []
        list_longest_streak_task = []

        # Checks if the request was a POST method
        if request.method == 'POST':
            # Checks if the "periodicity" form was sent
            if request.form.get('periodicity'):
                # Stores the user input of the periodicity and calls the function from the analytics module
                periodicity = request.form.get('periodicity')
                list_periodicity = same_periodicity(periodicity)

            # Checks if the "task" form was sent
            if request.form.get('task'):
                # Stores the user input of the task and calls the function from the analytics module
                task = request.form.get('task')
                list_longest_streak_task = longest_streak_task(task)

        # Renders the html of analytics.html in the templates folder and passes variables to the html file
        return render_template("analytics.html", login_status=g.habit.login_status, list_periodicity_html=list_periodicity, list_longest_streak_html=list_longest_streak, list_longest_streak_task_html=list_longest_streak_task)


@views.route('/habits', methods=['GET', 'POST'])
def habits():
    """Manages the habits page"""
    # Checks for the login status
    if g.habit.login_status == False:
        flash('Please login to access this page', category="error")
        return redirect(url_for('views.login'))
    else:
        # Checks if the request was a POST method
        if request.method == 'POST':
            # Stores the user input of the form
            task = request.form.get('task')
            periodicity = request.form.get('periodicity')

            # Checks if the task field is empty
            if len(task) < 1:
                flash('The task field cannot be empty', category="error")

            # Checks if the periodicity field is empty
            elif len(periodicity) < 1:
                flash('The periodicity field cannot be empty', category="error")

            # Checks if the periodicity is a number
            elif not(periodicity.isnumeric()):
                flash('The periodicity must a number', category="error")

            # Checks if the task/habit already exists
            elif any(habit_data['task'] == task for habit_data in g.habit.habit_data):
                flash('The habit already exsists!', category="error")

            # If all requirements are met a hbait is created
            else:
                # Calls the create_habit function from habit and passes the form
                # Data is then saved onto the .json file
                today = date.today()
                g.habit.create_habit({'task': task, 'periodicity': periodicity, 'last_checked': today.strftime(
                    "%d/%m/%Y"), 'longest_streak': 0, 'streak': 0})
                g.habit.save_data()
                flash('Habit created!', category="success")

        # Renders the html of habits.html in the templates folder and passes variables to the html file
        return render_template("habits.html", login_status=g.habit.login_status, habit_data=g.habit.habit_data)


@views.route("/delete/<task>")
def delete(task):
    # Checks for the login status
    if g.habit.login_status == False:
        flash('Please login to access this page', category="error")
        return redirect(url_for('views.login'))
    else:
        """Manages the deletion of a habit"""
        # Parses the html string and passes the task into the delete_habit function
        # Data is then saved onto the .json file
        g.habit.delete_habit(task)
        g.habit.save_data()

        # Redirects the user to the views.habits route
        return redirect(url_for('views.habits'))


@views.route("/check/<task>")
def check(task):
    # Checks for the login status
    if g.habit.login_status == False:
        flash('Please login to access this page', category="error")
        return redirect(url_for('views.login'))
    else:
        """Manages the check of a habit"""
        # Parses the html string and passes the task into the check_habit function
        # Data is then saved onto the .json file
        g.habit.check_habit(task)
        g.habit.save_data()

        # Redirects the user to the views.habits route
        return redirect(url_for('views.habits'))
