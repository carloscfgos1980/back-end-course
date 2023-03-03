## Inserting Rows with the ORM
When using the ORM, the Session object is responsible for constructing Insert constructs and emitting them for us in a transaction. The way we instruct the Session to do so is by adding object entries to it; the Session then makes sure these new entries will be emitted to the database when they are needed, using a process known as a flush.

## Instances of Classes represent Rows
Whereas in the previous example we emitted an INSERT using Python dictionaries to indicate the data we wanted to add, with the ORM we make direct use of the custom Python classes we defined, back at Defining Table Metadata with the ORM. At the class level, the User and Address classes served as a place to define what the corresponding database tables should look like. These classes also serve as extensible data objects that we use to create and manipulate rows within a transaction as well. Below we will create two User objects each representing a potential database row to be INSERTed:

>>> squidward = User(name="squidward", fullname="Squidward Tentacles")
>>> krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

We are able to construct these objects using the names of the mapped columns as keyword arguments in the constructor. This is possible as the User class includes an automatically generated __init__() constructor that was provided by the ORM mapping so that we could create each object using column names as keys in the constructor.

In a similar manner as in our Core examples of Insert, we did not include a primary key (i.e. an entry for the id column), since we would like to make use of the auto-incrementing primary key feature of the database, SQLite in this case, which the ORM also integrates with. The value of the id attribute on the above objects, if we were to view it, displays itself as None:

>>> squidward
User(id=None, name='squidward', fullname='Squidward Tentacles')

The None value is provided by SQLAlchemy to indicate that the attribute has no value as of yet. SQLAlchemy-mapped attributes always return a value in Python and don’t raise AttributeError if they’re missing, when dealing with a new object that has not had a value assigned.

At the moment, our two objects above are said to be in a state called transient - they are not associated with any database state and are yet to be associated with a Session object that can generate INSERT statements for them.