from flask import make_response
from flask import render_template
'''If you want to get hold of the resulting response object inside the view you can use the make_response() function.

Imagine you have a view like this:
'''


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


'''You just need to wrap the return expression with make_response() and get the response object to modify it, then return it:'''


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
