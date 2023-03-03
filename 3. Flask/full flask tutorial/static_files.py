# Static Files
'''
Dynamic web applications also need static files. That’s usually where the CSS and JavaScript files are coming from . Ideally your web server is configured to serve them for you, but during development Flask can do that as well. Just create a folder called static in your package or next to your module and it will be available at / static on the application.

To generate URLs for static files, use the special 'static' endpoint name:
'''
from flask import render_template
url_for('static', filename='style.css')

'''The file has to be stored on the filesystem as static/style.css.'''

# Rendering Templates

'''
Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the HTML escaping on your own to keep the application secure. Because of that Flask configures the Jinja2 template engine for you automatically.
'''


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
