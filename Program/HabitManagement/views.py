#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html")