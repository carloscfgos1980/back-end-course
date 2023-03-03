## Declaring Mapped Classes
The Base object above is a Python class which will serve as the base class for the ORM mapped classes we declare. We can now define ORM mapped classes for the user and address table in terms of new classes User and Address:

>>> from sqlalchemy.orm import relationship
>>> class User(Base):
...     __tablename__ = "user_account"
...
...     id = Column(Integer, primary_key=True)
...     name = Column(String(30))
...     fullname = Column(String)
...
...     addresses = relationship("Address", back_populates="user")
...
...     def __repr__(self):
...         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

>>> class Address(Base):
...     __tablename__ = "address"
...
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey("user_account.id"))
...
...     user = relationship("User", back_populates="addresses")
...
...     def __repr__(self):
...         return f"Address(id={self.id!r}, email_address={self.email_address!r})"

The above two classes are now our mapped classes, and are available for use in ORM persistence and query operations, which will be described later. But they also include Table objects that were generated as part of the declarative mapping process, and are equivalent to the ones that we declared directly in the previous Core section. We can see these Table objects from a declarative mapped class using the .__table__ attribute:

>>> User.__table__
Table('user_account', MetaData(),
    Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False),
    Column('name', String(length=30), table=<user_account>),
    Column('fullname', String(), table=<user_account>), schema=None)

This Table object was generated from the declarative process based on the .__tablename__ attribute defined on each of our classes, as well as through the use of Column objects assigned to class-level attributes within the classes. These Column objects can usually be declared without an explicit “name” field inside the constructor, as the Declarative process will name them automatically based on the attribute name that was used.

See also

Declarative Mapping - overview of Declarative class mapping

## Other Mapped Class Details
For a few quick explanations for the classes above, note the following attributes:

the classes have an automatically generated __init__() method - both classes by default receive an __init__() method that allows for parameterized construction of the objects. We are free to provide our own __init__() method as well. The __init__() allows us to create instances of User and Address passing attribute names, most of which above are linked directly to Column objects, as parameter names:

>>> sandy = User(name="sandy", fullname="Sandy Cheeks")

More detail on this method is at Default Constructor.

we provided a __repr__() method - this is fully optional, and is strictly so that our custom classes have a descriptive string representation and is not otherwise required:

>>> sandy
User(id=None, name='sandy', fullname='Sandy Cheeks')

An interesting thing to note above is that the id attribute automatically returns None when accessed, rather than raising AttributeError as would be the usual Python behavior for missing attributes.

we also included a bidirectional relationship - this is another fully optional construct, where we made use of an ORM construct called relationship() on both classes, which indicates to the ORM that these User and Address classes refer to each other in a one to many / many to one relationship. The use of relationship() above is so that we may demonstrate its behavior later in this tutorial; it is not required in order to define the Table structure.

## Emitting DDL to the database
This section is named the same as the section Emitting DDL to the Database discussed in terms of Core. This is because emitting DDL with our ORM mapped classes is not any different. If we wanted to emit DDL for the Table objects we’ve created as part of our declaratively mapped classes, we still can use MetaData.create_all() as before.

In our case, we have already generated the user and address tables in our SQLite database. If we had not done so already, we would be free to make use of the MetaData associated with our registry and ORM declarative base class in order to do so, using MetaData.create_all():

# emit CREATE statements given ORM registry
mapper_registry.metadata.create_all(engine)

# the identical MetaData object is also present on the
# declarative base
Base.metadata.create_all(engine)


## Combining Core Table Declarations with ORM Declarative
As an alternative approach to the mapping process shown previously at Declaring Mapped Classes, we may also make use of the Table objects we created directly in the section Setting up MetaData with Table objects in conjunction with declarative mapped classes from a declarative_base() generated base class.

This form is called hybrid table, and it consists of assigning to the .__table__ attribute directly, rather than having the declarative process generate it:

mapper_registry = registry()
Base = mapper_registry.generate_base()


class User(Base):
    __table__ = user_table

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User({self.name!r}, {self.fullname!r})"


class Address(Base):
    __table__ = address_table

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address({self.email_address!r})"

Note

The above example is an alternative form to the mapping that’s first illustrated previously at Declaring Mapped Classes. This example is for illustrative purposes only, and is not part of this tutorial’s “doctest” steps, and as such does not need to be run for readers who are executing code examples. The mapping here and the one at Declaring Mapped Classes produce equivalent mappings, but in general one would use only one of these two forms for particular mapped class.

The above two classes are equivalent to those which we declared in the previous mapping example.

The traditional “declarative base” approach using __tablename__ to automatically generate Table objects remains the most popular method to declare table metadata. However, disregarding the ORM mapping functionality it achieves, as far as table declaration it’s merely a syntactical convenience on top of the Table constructor.

We will next refer to our ORM mapped classes above when we talk about data manipulation in terms of the ORM, in the section Inserting Rows with the ORM.

## Table Reflection
To round out the section on working with table metadata, we will illustrate another operation that was mentioned at the beginning of the section, that of table reflection. Table reflection refers to the process of generating Table and related objects by reading the current state of a database. Whereas in the previous sections we’ve been declaring Table objects in Python and then emitting DDL to the database, the reflection process does it in reverse.

As an example of reflection, we will create a new Table object which represents the some_table object we created manually in the earlier sections of this document. There are again some varieties of how this is performed, however the most basic is to construct a Table object, given the name of the table and a MetaData collection to which it will belong, then instead of indicating individual Column and Constraint objects, pass it the target Engine using the Table.autoload_with parameter:

>>> some_table = Table("some_table", metadata_obj, autoload_with=engine)
BEGIN (implicit)
PRAGMA main.table_...info("some_table")
[raw sql] ()
SELECT sql FROM  (SELECT * FROM sqlite_master UNION ALL   SELECT * FROM sqlite_temp_master) WHERE name = ? AND type = 'table'
[raw sql] ('some_table',)
PRAGMA main.foreign_key_list("some_table")
...
PRAGMA main.index_list("some_table")
...
ROLLBACK

At the end of the process, the some_table object now contains the information about the Column objects present in the table, and the object is usable in exactly the same way as a Table that we declared explicitly:

>>> some_table
Table('some_table', MetaData(),
    Column('x', INTEGER(), table=<some_table>),
    Column('y', INTEGER(), table=<some_table>),
    schema=None)