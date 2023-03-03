## DATABASE

# Steps

1. __init__.py:
1.1 Import <SQLAlchemy>
from flask_sqlalchemy import SQLAlchemy

1.2 Call the database function:
db = SQLAlchemy()

1.3 Give a name to the database. Note it is with capital letters.
DB_NAME = "database.db"

1.4 Tell the app where this data base is located:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

1.5 Connect the database with the app
    db.init_app(app)

2. models.py:
2.1 import db (database inside __init__.py)
from . import db
* (.) in this case indicate that the location is inside the folder. It would be the same as saying:
from website import db

2.2 Create the class for the user:
2.2.1 Import a module to help us to handle the data from the users
from flask_login import UserMixin

2.2.2 Create the class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
* the id will be always be an integer (num) and the primary key. This helps to identify the object
* email = db.Column(db.String(150), unique=True). Means that the longer email extantion can be 150 characters, is a String and it has to be unique

2.3 Create the class for the notes:
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    
2.3.1 Import a function from <sqlalchemy> to get the time automatically. This can be with another modeule but this guy like to show up... anyway this is how is done:

from sqlalchemy.sql import func
2.3.2 Inside the <class Notes>. Create another variable to storage the time, using <sqlalchemy>
date = db.Column(db.DateTime(timezone=True), default=func.now())

2.3.3 USe the foreign key to connect more than one object (notes) to the user:
user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
* even when the class is with capital letters (class User), with the foreign key is lower case.

class Note look like this:

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

2.4 Inside <class User>, stablish a relationship (connection) between <class USer> and <class Note>:
notes = db.relationship('Note')
* In this case it is used uppercase just like we defined the class.
<class User> looks like this

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')