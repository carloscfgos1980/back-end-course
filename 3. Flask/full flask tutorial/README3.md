# Static Files
Dynamic web applications also need static files. That’s usually where the CSS and JavaScript files are coming from. Ideally your web server is configured to serve them for you, but during development Flask can do that as well. Just create a folder called static in your package or next to your module and it will be available at /static on the application.

To generate URLs for static files, use the special 'static' endpoint name:

url_for('static', filename='style.css')
The file has to be stored on the filesystem as static/style.css.

# Rendering Templates
Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the HTML escaping on your own to keep the application secure. Because of that Flask configures the Jinja2 template engine for you automatically.

Templates can be used to generate any type of text file. For web applications, you’ll primarily be generating HTML pages, but you can also generate markdown, plain text for emails, any anything else.

For a reference to HTML, CSS, and other web APIs, use the MDN Web Docs.

https://developer.mozilla.org/en-US/

To render a template you can use the render_template() method. All you have to do is provide the name of the template and the variables you want to pass to the template engine as keyword arguments. Here’s a simple example of how to render a template:

https://flask.palletsprojects.com/en/2.2.x/api/#flask.render_template


from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
Flask will look for templates in the templates folder. So if your application is a module, this folder is next to that module, if it’s a package it’s actually inside your package:

Case 1: a module:

/application.py
/templates
    /hello.html
Case 2: a package:

/application
    /__init__.py
    /templates
        /hello.html
For templates you can use the full power of Jinja2 templates. Head over to the official Jinja2 Template Documentation for more information.

https://jinja.palletsprojects.com/en/3.1.x/templates/

Here is an example template:

<!doctype html>
<title>Hello from Flask</title>
{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello, World!</h1>
{% endif %}
Inside templates you also have access to the config, request, session and g 1 objects as well as the url_for() and get_flashed_messages() functions.

Templates are especially useful if inheritance is used. If you want to know how that works, see Template Inheritance. 
https://flask.palletsprojects.com/en/2.2.x/patterns/templateinheritance/


Basically template inheritance makes it possible to keep certain elements on each page (like header, navigation and footer).

Automatic escaping is enabled, so if name contains HTML it will be escaped automatically. If you can trust a variable and you know that it will be safe HTML (for example because it came from a module that converts wiki markup to HTML) you can mark it as safe by using the Markup class or by using the |safe filter in the template. Head over to the Jinja 2 documentation for more examples.

Here is a basic introduction to how the Markup class works:

https://flask.palletsprojects.com/en/2.2.x/api/#flask.Markup


>>> from markupsafe import Markup
>>> Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
Markup('<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')
>>> Markup.escape('<blink>hacker</blink>')
Markup('&lt;blink&gt;hacker&lt;/blink&gt;')
>>> Markup('<em>Marked up</em> &raquo; HTML').striptags()
'Marked up » HTML'
Changelog
1
Unsure what that g object is? It’s something in which you can store information for your own needs. See the documentation for flask.g and Using SQLite 3 with Flask.