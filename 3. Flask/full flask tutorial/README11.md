# Message Flashing
Good applications and user interfaces are all about feedback. If the user does not get enough feedback they will probably end up hating the application. Flask provides a really simple way to give feedback to a user with the flashing system. The flashing system basically makes it possible to record a message at the end of a request and access it on the next (and only the next) request. This is usually combined with a layout template to expose the message.

To flash a message use the flash() method, to get hold of the messages you can use get_flashed_messages() which is also available in the templates. See Message Flashing for a full example.

# Logging
Changelog
Sometimes you might be in a situation where you deal with data that should be correct, but actually is not. For example you may have some client-side code that sends an HTTP request to the server but it’s obviously malformed. This might be caused by a user tampering with the data, or the client code failing. Most of the time it’s okay to reply with 400 Bad Request in that situation, but sometimes that won’t do and the code has to continue working.

You may still want to log that something fishy happened. This is where loggers come in handy. As of Flask 0.3 a logger is preconfigured for you to use.

Here are some example log calls:

app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
The attached logger is a standard logging Logger, so head over to the official logging docs for more information.

See Handling Application Errors.

# Hooking in WSGI Middleware
To add WSGI middleware to your Flask application, wrap the application’s wsgi_app attribute. For example, to apply Werkzeug’s ProxyFix middleware for running behind Nginx:

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
Wrapping app.wsgi_app instead of app means that app still points at your Flask application, not at the middleware, so you can continue to use and configure app directly.

# Using Flask Extensions
Extensions are packages that help you accomplish common tasks. For example, Flask-SQLAlchemy provides SQLAlchemy support that makes it simple and easy to use with Flask.

For more on Flask extensions, see Extensions.

https://flask.palletsprojects.com/en/2.2.x/extensions/


Deploying to a Web Server
Ready to deploy your new Flask app? See Deploying to Production.

https://flask.palletsprojects.com/en/2.2.x/deploying/
