#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
#The authentification and the normal views should be seperated
from flask import Blueprint, render_template, request, flash, json, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from HabitManagement import settings
from .habits import Habit
from os import path, listdir

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if path.isfile(f"./Data/{username}.json"):
            with open(f"Data/{username}.json", "r") as file:
                user_json = json.loads(file.read())

            json_password = user_json['user_data'][0]['password']

            if check_password_hash(json_password, password):
                flash('Loged in successfully', category="success")
                settings.login_status = True
                settings.current_user = username

                for habit_data in user_json['habit_data']:
                    for task, periodicity in habit_data['task'] and habit_data['periodicity']:
                        new_habit = Habit(task, periodicity)

                return redirect(url_for('views.home'))
            else:
                flash('The password is wrong!', category="error")

        else:
            flash('The username does not exist!', category="error")

    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    settings.login_status = False
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        def registration(*args, **kwargs):
            user_json = {"user_data" : [], "habit_data" : []}
            registration_data = {"email" : email, "username": username, "password" : generate_password_hash(password1, method='sha256')}
            user_json['user_data'].append(registration_data)
            jsonStr = json.dumps(user_json, indent = 4, sort_keys = False)

            with open(f"Data/{username}.json", "w") as file:
                file.write(jsonStr)      

        if len(email) < 4:
            flash('Email must be greater than 3 characters!', category="error")
            
        elif len(username) < 1:
            flash('Username must be at least 1 character!', category="error")

        elif password1 != password2:
            flash('The passwords do not match!', category="error")

        elif len(password1) < 4:
            flash('The password must be at least 4 characters!', category="error")

        elif path.isfile(f"./Data/{username}.json"):
            flash('This username already exists!', category="error")

        elif len(listdir('./Data')) != 0:
            for filename in listdir('./Data'):
                with open(f"./Data/{filename}") as currentFile:
                    text = currentFile.read()
                    if email in text:
                        flash('This email adress already exists!', category="error")
                    else:
                        flash('Account created!', category="success")
                        registration(email, username, password1)
                        settings.login_status = True
                        settings.current_user = username
                        return redirect(url_for('views.home'))
                        
        else:
            flash('Account created!', category="success")
            registration(email, username, password1)
            settings.login_status = True
            settings.current_user = username
            return redirect(url_for('views.home'))
            
    return  render_template("register.html")

