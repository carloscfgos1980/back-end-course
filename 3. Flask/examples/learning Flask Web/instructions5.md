## DATABASE CREATION

* The tutorial shows how to create a database file (.db) but I can't make work so what I did was create the file manually, it has to be in the same root of main.py

# Steps
1. Import module to create database:
from flask_sqlalchemy import SQLAlchemy

2. variable to store the name of the database:

DB_NAME = "database.db"

3. Call <SQLAlchemy> function:
db = SQLAlchemy()

4. Configuration of the database:
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

5. Initiate the database:
    db.init_app(app)

6. Import the classes that will be incorporate as tables to database:
 from .models import User, Note
* This is only necessary in case that these clases are in different file.

7. Create data base
     with app.app_context():
        db.create_all()

* This is the last step, is has to be after the classe models so it will create the tables based in those class Models
