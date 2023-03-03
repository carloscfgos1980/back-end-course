## Using an ORM: Peewee and Python

SQL is extremely powerful, since it can handle lots of different types of queries. SQL has some downsides as well: 
* Queries are written in "plain" text, making them prone to human error. Wrongly written queries can even result in the corruption of a database!
* Writing queries requires a lot of boilerplate(opens in a new tab), which is tedious for developers.

To mitigate these problems, many developers opt to use an <Object Relational Mapper> (ORM) for short. This module will teach you about Peewee, a lightweight ORM for Python. 

# What does an ORM do?

An ORM is an abstraction layer over SQL. At its core it is a way to compose database queries, without having to write SQL. At its core, an ORM facilitates a number of things: 1. A way to connect to a database 2. Base classes that facilitate data model management 3. Methods that translate to SQL queries

ORM's increase the speed with which you can develop because you do not have to write long SQL queries for simple operations. Where in SQL you might write something like SELECT * from item WHERE id=1, then you would have to select the first record that the database returns, and finally you would have to translate this data into a python object. An ORM would let you do something like Item.get(id=1) for the same result. An ORM also adds a layer of safety; if your SQL query uses parameters, you could be prone to SQL injection if you do not properly deal with strings. An ORM has this specific safety built into it, so it is much harder to corrupt your database. Next to making it easier to query data from the database, an ORM facilitates a way to translate data from the database to object in Python. Working with defined objects is a better development experience than working with records from a database; it allows you to inspect all the properties and methods that belong to a certain data model.

The main weakness of an ORM is that it is prone to introducing inefficienscies in the way a database is queried; due to the nature of the composability of queries, an ORM might do multiple roundtrips to the database where this is not necessary.

# Using Peewee
The ORM that will be used in this module is Peewee, it is a lightweight ORM for Python. We will use it in conjunction with an SQLite3 database.

o install peewee, use pip: pip install peewee

# Connecting to a database
Peewee allows us to connect to different types of databases. We are specifically interested in connecting to an SQLite database. The peewee docs on connections(opens in a new tab) illustrate how to do this:

http://docs.peewee-orm.com/en/latest/peewee/database.html

from peewee import *

db = SqliteDatabase('app.db')

# Defining data models
The peewee quickstart(opens in a new tab) example provides a good example of how to define a model: 

http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#model-definition

from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db


There are a number of elements to this code.
class Person(Model):
    ...



This part basically says "inherit all functionality from Model". This adds all the querying functionality to the Person class, allowing us to use something like Person.select() without having to define a select method.

name = CharField()
birthday = DateField()

These proprety definitions determine what fields are created in the SQLite database. In this case, we are creating 2 fields for Person with the VARCHAR and DATE sql types. This also translates back to the correct types in python, meaning that when we work with the Person object, name will be of type str and birthday will be of type datetime.

db = SqliteDatabase('app.db')

class Person(Model):
    ...
    class Meta:
        database = db


Finally the Meta class of a model allows us to specify metadata about the model. The only required metadata option is database, this indicates in which database the data for this model should be stored. You can find other Meta options in the docs

http://docs.peewee-orm.com/en/latest/peewee/models.html#model-options-and-table-metadata


# Creating the tables
After defining the models with which we want to work, we have to initialize the database by creating tables for these models. The suggested way is to make a utility function that creates the tables and to run it the first time you use the database. An example can be found in the docs(opens in a new tab).

http://docs.peewee-orm.com/en/latest/peewee/example.html#creating-tables

* Note: Every time you run this function, you will reset the database

database = SqliteDatabase('app.db')

def create_tables():
    with database:
        database.create_tables([User, Relationship, Message])

Then open a python shell and execute the function. 

# Making database queries
Peewee provides interfaces for most SQL operations. The SELECT operation can be executed with the .select() method for instance. Below are some examples, but a complete overview of the avaialble methods can be found in the documentation
http://docs.peewee-orm.com/en/latest/peewee/querying.html

# create a person in the database
Person.create(name="Jimmy", birthday="01-01-1980") 

# retrieve a single person by name
jimmy = Person.get(Person.name == "Jimmy")

# update a person in the database
jimmy.name = "James"
jimmy.save()

# delete a person
jimmy.delete_instance()

* Note: Peewee is a large package with lots of functionality. The best way to learn using it is to just use it. The documentation is an invaluable source of examples and explanations. It is worth taking the time to play around with all the examples in order to understand how the various query methods work. It is rich in practical examples and comprehensive explanations.