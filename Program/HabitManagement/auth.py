#A blueprint is an object that allows defining application functions without requiring an application object ahead of time.
#The authentification and the normal views should be seperated
from flask import Blueprint, render_template, request, flash

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
            flash('Email must be at least 4 characters!', category="error")
        elif len(UserName) < 2:
            flash('Username must be at least 2 characters!', category="error")
        elif password1 != password2:
            flash('The passwords do not match!', category="error")
        elif len(password1) < 4:
            flash('The password must at least 4 characters!', category="error")
        else:
            flash('Account created!', category="success")

    return render_template("register.html")