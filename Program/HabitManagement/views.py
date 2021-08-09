#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "<h1>Test</h1>"