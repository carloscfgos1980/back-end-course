## FLASK

# A Minimal Applicatio

A minimal Flask application looks something like this:

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
So what did that code do?

First we imported the Flask class. An instance of this class will be our WSGI application.
Next we create an instance of this class. The first argument is the name of the application’s module or package. __name__ is a convenient shortcut for this that is appropriate for most cases. This is needed so that Flask knows where to look for resources such as templates and static files.
We then use the route() decorator to tell Flask what URL should trigger our function.
The function returns the message we want to display in the user’s browser. The default content type is HTML, so HTML in the string will be rendered by the browser.
Save it as hello.py or something similar. Make sure to not call your application flask.py because this would conflict with Flask itself.

To run the application, use the flask command or python -m flask. You need to tell the Flask where your application is with the --app option.

$ flask --app hello run


# Externally Visible Server

If you run the server you will notice that the server is only accessible from your own computer, not from any other in the network. This is the default because in debugging mode a user of the application can execute arbitrary Python code on your computer.

If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding --host=0.0.0.0 to the command line:

$ flask run --host=0.0.0.0
This tells your operating system to listen on all public IPs.


Debug Mode
The flask run command can do more than just start the development server. By enabling debug mode, the server will automatically reload if code changes, and will show an interactive debugger in the browser if an error occurs during a request.

Warning
The debugger allows executing arbitrary Python code from the browser. It is protected by a pin, but still represents a major security risk. Do not run the development server or debugger in a production environment.
To enable debug mode, use the --debug option.

$ flask --app hello --debug run


HTML Escaping
When returning HTML (the default response type in Flask), any user-provided values rendered in the output must be escaped to protect from injection attacks. HTML templates rendered with Jinja, introduced later, will do this automatically.

escape(), shown here, can be used manually. It is omitted in most examples for brevity, but you should always be aware of how you’re using untrusted data.

from markupsafe import escape

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"
If a user managed to submit the name <script>alert("bad")</script>, escaping causes it to be rendered as text, rather than running the script in the user’s browser.

<name> in the route captures a value from the URL and passes it to the view function. These variable rules are explained below.

Routing
Modern web applications use meaningful URLs to help users. Users are more likely to like a page and come back if the page uses a meaningful URL they can remember and use to directly visit a page.

Use the route() decorator to bind a function to a URL.

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
You can do more! You can make parts of the URL dynamic and attach multiple rules to a function.

Variable Rules
You can add variable sections to a URL by marking sections with <variable_name>. Your function then receives the <variable_name> as a keyword argument. Optionally, you can use a converter to specify the type of the argument like <converter:variable_name>.

from markupsafe import escape

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
Converter types:

string
(default) accepts any text without a slash
int
accepts positive integers
float
accepts positive floating point values
path
like string but also accepts slashes
uuid
accepts UUID strings
