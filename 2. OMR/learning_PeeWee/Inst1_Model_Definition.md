## PeeWee tutorial
http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#model-definition


# Model Definition

Model classes, fields and model instances all map to database concepts:

Object	Corresponds to…
Model class	Database table
Field instance	Column on a table
Model instance	Row in a database table
When starting a project with peewee, it’s typically best to begin with your data model, by defining one or more Model classes:

from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.


There are lots of field types suitable for storing various types of data. Peewee handles converting between pythonic values and those used by the database, so you can use Python types in your code without having to worry.

Things get interesting when we set up relationships between models using foreign key relationships. This is simple with peewee:

class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # this model uses the "people.db" database


Now that we have our models, let’s connect to the database. Although it’s not necessary to open the connection explicitly, it is good practice since it will reveal any errors with your database connection immediately, as opposed to some arbitrary time later when the first query is executed. It is also good to close the connection when you are done – for instance, a web app might open a connection when it receives a request, and close the connection when it sends the response.

db.connect()

We’ll begin by creating the tables in the database that will store our data. This will create the tables with the appropriate columns, indexes, sequences, and foreign key constraints:

db.create_tables([Person, Pet])

# Relation between tables
Now we have stored 3 people in the database. Let’s give them some pets. Grandma doesn’t like animals in the house, so she won’t have any, but Herb is an animal lover:

bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

