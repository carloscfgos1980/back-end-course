# Shows only Log in and Sign up if the user is not logged in

1. auth.py:
1.1 Import module of <current_user>:
from flask_login import login_user, login_required, logout_user, current_user

1.2 In  @auth.route('/login', methods=['GET', 'POST']), return <current_user>:
    return render_template("login.html", title="Log in", user=current_user)

1.3 In @auth.route('/sing-up', methods=['GET', 'POST']), return <current_user>:
    return render_template("sign_up.html", title="Sign up", user=current_user)

2. views.py:
2.1 Import module of <current_user>:
from flask_login import login_required, current_user

2.2 In @views.route('/', methods=['GET', 'POST']), return <current_user>:
    return render_template("home.html", user=current_user)

3. base.html:
3.1 In the NavBar. Condiction to show <Home> and <Log out> only is the user is Logged in:
                {% if user.is_authenticated %}
                <li class="nav-item active">
                    <a class="nav-link" href="/">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/logout">Log out</a>
                </li>
3.2 Else return <Log in> and <Sing Up>
              {% else %}
                <li class="nav-item">
                    <a class="nav-link" href="/login">Login</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/sing-up">Sign up</a>
                </li>
                {% endif %}

* the whole condiction in the NavBar looks like this:

            <ul class="navbar-nav">
                {% if user.is_authenticated %}
                <li class="nav-item active">
                    <a class="nav-link" href="/">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/logout">Log out</a>
                </li>
                {% else %}
                <li class="nav-item">
                    <a class="nav-link" href="/login">Login</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/sing-up">Sign up</a>
                </li>
                {% endif %}
            </ul>