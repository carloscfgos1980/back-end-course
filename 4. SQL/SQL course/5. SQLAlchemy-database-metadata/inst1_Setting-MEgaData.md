## Working with Database Metadata
With engines and SQL execution down, we are ready to begin some Alchemy. The central element of both SQLAlchemy Core and ORM is the SQL Expression Language which allows for fluent, composable construction of SQL queries. The foundation for these queries are Python objects that represent database concepts like tables and columns. These objects are known collectively as database metadata.

The most common foundational objects for database metadata in SQLAlchemy are known as MetaData, Table, and Column. The sections below will illustrate how these objects are used in both a Core-oriented style as well as an ORM-oriented style.


## Setting up MetaData with Table objects
When we work with a relational database, the basic structure that we create and query from is known as a table. In SQLAlchemy, the “table” is represented by a Python object similarly named Table.

To start using the SQLAlchemy Expression Language, we will want to have Table objects constructed that represent all of the database tables we are interested in working with. Each Table may be declared, meaning we explicitly spell out in source code what the table looks like, or may be reflected, which means we generate the object based on what’s already present in a particular database. The two approaches can also be blended in many ways.

Whether we will declare or reflect our tables, we start out with a collection that will be where we place our tables known as the MetaData object. This object is essentially a facade around a Python dictionary that stores a series of Table objects keyed to their string name. Constructing this object looks like:

>>> from sqlalchemy import MetaData
>>> metadata_obj = MetaData()

Having a single MetaData object for an entire application is the most common case, represented as a module-level variable in a single place in an application, often in a “models” or “dbschema” type of package. There can be multiple MetaData collections as well, however it’s typically most helpful if a series of Table objects that are related to each other belong to a single MetaData collection.

Once we have a MetaData object, we can declare some Table objects. This tutorial will start with the classic SQLAlchemy tutorial model, that of the table user, which would for example represent the users of a website, and the table address, representing a list of email addresses associated with rows in the user table. We normally assign each Table object to a variable that will be how we will refer to the table in application code:

>>> from sqlalchemy import Table, Column, Integer, String
>>> user_table = Table(
...     "user_account",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("name", String(30)),
...     Column("fullname", String),
... )

We can observe that the above Table construct looks a lot like a SQL CREATE TABLE statement; starting with the table name, then listing out each column, where each column has a name and a datatype. The objects we use above are:

Table - represents a database table and assigns itself to a MetaData collection.

Column - represents a column in a database table, and assigns itself to a Table object. The Column usually includes a string name and a type object. The collection of Column objects in terms of the parent Table are typically accessed via an associative array located at Table.c:

>>> user_table.c.name
Column('name', String(length=30), table=<user_account>)

>>> user_table.c.keys()
['id', 'name', 'fullname']

Integer, String - these classes represent SQL datatypes and can be passed to a Column with or without necessarily being instantiated. Above, we want to give a length of “30” to the “name” column, so we instantiated String(30). But for “id” and “fullname” we did not specify these, so we can send the class itself.

See also

The reference and API documentation for MetaData, Table and Column is at Describing Databases with MetaData. The reference documentation for datatypes is at SQL Datatype Objects.

In an upcoming section, we will illustrate one of the fundamental functions of Table which is to generate DDL on a particular database connection. But first we will declare a second Table.