#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
#The authentification and the normal views should be seperated
from flask import Blueprint, render_template, request, flash, json, jsonify
import os.path

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text="Testing", user="Tim")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        UserName = request.form.get('UserName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        

        if len(email) < 4:
            flash('Email must be greater than 3 characters!', category="error")
        elif len(UserName) < 1:
            flash('Username must be at least 1 character!', category="error")
        elif password1 != password2:
            flash('The passwords do not match!', category="error")
        elif len(password1) < 4:
            flash('The password must be at least 4 characters!', category="error")
        #elif 

        else:
            flash('Account created!', category="success")

            registration_data = {"email" : email, "username": UserName, "password" : password1}
            jsonStr = json.dumps(registration_data, indent = 4)

            with open("Data/User_data.json", "w") as user_data:
                user_data.write(jsonStr)

    return  render_template("register.html")