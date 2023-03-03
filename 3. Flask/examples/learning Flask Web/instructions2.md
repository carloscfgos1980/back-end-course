# Templates

1. Inside folder "templates". Create base.html
* This is a way to create a website without JavaScript using Jinjag whih also allows as to write python inside html
* the content will be injected to this file from python files or from child html components.
1.1 Dynamic way to change the title of this html when a another child html component is injected
<title>{% block title %}Home{% endblock %}</title>

1.2 script src gives us access to bootstrap and also to the files inside static folder. In this case is a javascript file but it could be also a css file. This <script src> are placed at the buttonof the page
This is the one for the static:
<script type="text/javascript" src="{{ url_for('static', filename='index.js') }}"></script>
* {{}} Means we are going to write a python expressionwith double curly brackets in a HTML file.

1.3 Create a nav bar with bootstrap
* the nav bar codes in base.html from the github has a problem. It had to copy the codes again from bootstrap
1.4 Read bootstrap documentation in rder to copy the links to base.html

1.5 sign_up.html:
Create a form from bootstrap with post method

1.6 login.html:
Create a form from bootstrap with post method



