#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")