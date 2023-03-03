# Unique URLs / Redirection Behavior

'''The following two rules differ in their use of a trailing slash'''


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


'''
The canonical URL for the projects endpoint has a trailing slash. It’s similar to a folder in a file system. If you access the URL without a trailing slash (/projects), Flask redirects you to the canonical URL with the trailing slash (/projects/).

The canonical URL for the about endpoint does not have a trailing slash. It’s similar to the pathname of a file. Accessing the URL with a trailing slash (/about/) produces a 404 “Not Found” error. This helps keep URLs unique for these resources, which helps search engines avoid indexing the same page twice
'''


# URL Building

'''
Why would you want to build URLs using the URL reversing function url_for() instead of hard-coding them into your templates?

Reversing is often more descriptive than hard-coding the URLs.
You can change your URLs in one go instead of needing to remember to manually change hard-coded URLs.
URL building handles escaping of special characters transparently.
The generated paths are always absolute, avoiding unexpected behavior of relative paths in browsers.
If your application is placed outside the URL root, for example, in /myapplication instead of /, url_for() properly handles that for you.
'''


@app.route('/')
def index():
    return 'index'


@app.route('/login')
def login():
    return 'login'


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

# HTTP Methods


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


'''
The example above keeps all methods for the route within one function, which can be useful if each part uses some common data.

You can also separate views for different methods into different functions. Flask provides a shortcut for decorating such routes with get(), post(), etc. for each common HTTP method.
'''


@app.get('/login')
def login_get():
    return show_the_login_form()


@app.post('/login')
def login_post():
    return do_the_login()
