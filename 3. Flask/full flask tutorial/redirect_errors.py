

from flask import render_template
from flask import abort, redirect, url_for

# Redirects and Errors
'''
To redirect a user to another endpoint, use the redirect() function
to abort a request early with an error code, use the abort() function:
'''


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


'''By default a black and white error page is shown for each error code. If you want to customize the error page, you can use the errorhandler() decorator:'''


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
