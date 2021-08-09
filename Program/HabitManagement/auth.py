#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
#The authentification and the normal views should be seperated
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>login</p>"

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/register')
def register():
    return "<p>register</p>"