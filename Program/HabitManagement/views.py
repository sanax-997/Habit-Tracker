#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
from flask import Blueprint, render_template, request, flash, json
from HabitManagement import settings

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", login_status = settings.login_status)

@views.route('/analytics')
def analytics():
    return render_template("analytics.html", login_status = settings.login_status)

@views.route('/habits', methods=['GET', 'POST'])
def habits():
    if request.method == 'POST':
        task = request.form.get('task')
        periodicity = request.form.get('periodicity')
        print(task, periodicity)

    return render_template("habits.html", login_status = settings.login_status, boolean=True)