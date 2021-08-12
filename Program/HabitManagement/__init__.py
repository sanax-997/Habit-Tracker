from flask import Flask


def create_app():
    #The create_app function initializes the Flask framework

    #The line app = Flask(__name__) is needed for Flask to know where the resources are located and creates an instance of the Flask class
    #The app.config function sets up a "Secret key", which encrypts the session data
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Vo@f!11pFP*mOEGO^@wCwXxDs2NAU^P*@FgOKm33i!w@U1YLaqeE!p#5$9wGVKlG1sgTj7C8l1r$yxH!osZRhzOmgzb@uA*2F1m'

    #To utilize blueprints they need to be registered in the initialization file
    #These are blueprints imported from the auth and views file. 
    from .views import views
    from .auth import auth

    #This code registers the blueprints, with a specified URL prefix
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app