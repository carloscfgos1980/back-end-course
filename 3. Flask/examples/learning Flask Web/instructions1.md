#   STEPS:
1. Install Flaks and Flask-SQLAlchemy. Check README.md
2. Create folder website that will work as a python package
3. website:
3.1 Create folder "static"
3.2 Create folder "templates"
3.3 Create 4 python files:
auth.py
models.py
views.py
_init__.py

4. __init__.py inside folder "website" allows this folder to be used as a python package

__init__.py:
4.1 Import flask
from flask import Flask
4.2 Create a function 
def create_app():
    app = Flask(__name__)

4.3 Inside this function will create a secret key for out app:
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

5. main.py
5.1 Import create app. We can do that coz __init__.py allows us to get access to all the functions inside this folder
from website import create_app

5.2 Storage create_app function in a variable
app = create_app()

5.3 Create a function in order to run the app from the VSCode
if __name__ == '__main__':
    app.run(debug=True)

6. views.py
6.1 Import Blueprint
from flask import Blueprint

6.2 Create a variable for views
views = Blueprint('views', __name__)

6.3 Create a Home route
@views.route('/')
def home():
    return "<h1> TEST </h1>"

7. auth.py
* Same as views.py:
7.1 Import Blueprint
from flask import Blueprint

7.2 Create a variable for views
auth = Blueprint('auth', __name__)


8 __init__.py:
8.1 Import views and auth
    from .views import views
    from .auth import auth

8.2 Registes Blueprints from views and auth. The <url_prefix='/'> help us to easily access to the web. DO NOT CHANGE
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

9 auth.py
9.1 define route for login
@auth.route('/login')
def login():
    return '<h1>Login</h1>

9.2 Define route for logout
@auth.route('/logout')
def logout():
    return '<h1>Logout</h1>'

9.3 Define route for sign up
@auth.route('/sing-up')
def sing_up():
    return '<h1>Sign up</h1>'
