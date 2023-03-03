## HTTP request

# STEPS
1. auth.py:
1.1 import request and flash modules
from flask import Blueprint, render_template, request, flash
<flash> is a built-in function to help us flash messages to the DOM

1.2 Declare the methods we are going to use
@auth.route('/sing-up', methods=['GET', 'POST'])

1.3 storage the values from the form:
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

1.4 Create an condiction so the input values are correct
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            flash('Account created!', category='success')
* check out the categories of the <flash>


2. base.html:
* The following codes are necessary to show the messages as alert.
2.1 using the buit-in function of "with"
2.2 condiction to check if there is any message
2.3 for loop for categories and messages.
2.4 condiction to check which type of the category is the flasj message
2.4 Use the alert from bootstrap
* This is kinda hard to read but it works! checkout base.html (line 37 - 57)


    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
    {% for category, message in messages %}
    {% if category == 'error' %}
    <div class="alert alert-danger alter-dismissable fade show" role="alert">
        {{ message }}
        <button type="button" class="close" data-dismiss="alert">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    {% else %}
    <div class="alert alert-success alter-dismissable fade show" role="alert">
        {{ message }}
        <button type="button" class="close" data-dismiss="alert">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    {% endif %}
    {% endfor %}
    {% endif %}
    {% endwith %}