# Create User & Login

# 1 Sign in Steps
auth.py:

1.1 Import the modules I need:
from flask import Blueprint, render_template, request, flash, redirect, url_for

1.2 Import User from models:
from .models import User

1.3 import database:
from . import db

1.4 import a module to handle secretly the passwords
from werkzeug.security import generate_password_hash, check_password_hash

1.5 Check if the user exist:
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
* Flash a message if the user already exist

1.6 Condictions required for log in:
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error'

1.7 in <else> condiction, create the new user:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
* we create a new user, is a form like a dictionary, then we add it to the data base by using add and commit, pretty similar to the command line when we update a github repository

1.8 Redirect to home page

1.8.1 Import from flask the modules redirect and url_for

1.8.2 return redirect(url_for('views.home'))

* Redirect is pretty straight forward, once the user is created it will redirect to home page.
* <url_for> allows as to not have to hard code ("/"), it could be like this:
return redirect("/")
But if we ever change the route of home, then we need to manually change the code, with <url_for>, it will get the new route autmatically.

The whole thing looks like this:
@auth.route('/sing-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", title="Sign up")



# 2 . Log in Steps:
2.1 Set get and Post method in the route function:
@auth.route('/login', methods=['GET', 'POST'])

2.2 Condiction to obtain the data from the form:
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

2.3 Check it the User exist:
        user = User.query.filter_by(email=email).first()
        if user:

2.4 If the user exist, then check password:

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", title="Log in", boolean=True)