# restring access without log in

1. auth.py
1.1 Impor modules:
from flask_login import login_user, login_required, logout_user, current_user

1.2 Implement <login_user> in @auth.route('/login', methods=['GET', 'POST']):
                login_user(user, remember=True)
* This is placed after checking that the password is alright and before redirecting.

1.3 Implement <login_user> in @auth.route('/sing-up', methods=['GET', 'POST']):
                login_user(user, remember=True)
* This is placed after commiting the new user and before redirecting.

1.4 Make the logout rout to be logged in (required) and redirect to login route once the user is log out. Like this:

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


2. ___init__.py:
2.1 Import modules to handle access to page:
from flask_login import LoginManager

2.2 Call <LogingManager> function:
    login_manager = LoginManager()

2.3 Set what would be the route if the user is not log in:
    login_manager.login_view = 'auth.login'

2.4 Initialize the Login Manager Function:
    login_manager.init_app(app)

2.5 Function to identify the user:
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


* All these codes are placed after the db.create_all(), right at the end before the last return. all together looks like this:

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

3. views.py
3.1 Import modules:
from flask_login import login_required, current_user

3.2 Add fectching methds to the route:
@views.route('/', methods=['GET', 'POST'])

3.3 Call <login_required> method inside @views.route:
@login_required