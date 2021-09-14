# The init.py file initialized all the variables and the framework needed to run the program

from flask import Flask


def create_app():
    """Initializes the Flask framework and global variables"""
    # The line app = Flask(__name__) is needed for Flask to know where the resources are located and creates an instance of the Flask class
    app = Flask(__name__)

    # The app.config function sets up a "Secret key", which encrypts the session data
    app.config['SECRET_KEY'] = 'Vo@f!11pFP*mOEGO^@wCwXxDs2NAU^P*@FgOKm33i!w@U1YLaqeE!p#5$9wGVKlG1sgTj7C8l1r$yxH!osZRhzOmgzb@uA*2F1m'

    # To utilize blueprints they need to be registered in the initialization file
    # These is the blueprint imported from the views file.
    from .views import views

    # This code registers the blueprints, with a specified URL prefix
    # A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
    app.register_blueprint(views, url_prefix='/')

    # Imports the global file
    from HabitManagement import globals as g

    # Initializes the login status function
    g.init_login_status()

    # Initializes the habit function
    g.init_habit()

    return app
