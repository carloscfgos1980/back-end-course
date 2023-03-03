from markupsafe import escape
from flask import Flask

app = Flask(__name__)


# minimal application
@app.route("/")
def hola_world():
    return "<p>Hola, World!</p>"


# HTML Escaping


'''
When returning HTML (the default response type in Flask), any user-provided values rendered in the output must be escaped to protect from injection attacks. HTML templates rendered with Jinja, introduced later, will do this automatically.

escape(), shown here, can be used manually. It is omitted in most examples for brevity, but you should always be aware of how you’re using untrusted data.
'''


@app.route("/<name>")
def hi(name):
    return f"Hello, {escape(name)}!"


# Routing
'''
Modern web applications use meaningful URLs to help users. Users are more likely to like a page and come back if the page uses a meaningful URL they can remember and use to directly visit a page.

Use the route() decorator to bind a function to a URL
'''


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello, World'


# Variable Rules


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
