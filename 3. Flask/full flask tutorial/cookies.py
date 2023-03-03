# Cookies

from flask import make_response
from flask import request


# Reading cookies:
@app.route('/')
def index():
    username = request.cookies.get('username')

    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.


# Storing cookies:
@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp
