Inserting Rows with Core
When using Core, a SQL INSERT statement is generated using the insert() function - this function generates a new instance of Insert which represents an INSERT statement in SQL, that adds new data into a table.

ORM Readers - The way that rows are INSERTed into the database from an ORM perspective makes use of object-centric APIs on the Session object known as the unit of work process, and is fairly different from the Core-only approach described here. The more ORM-focused sections later starting at Inserting Rows with the ORM subsequent to the Expression Language sections introduce this.

The insert() SQL Expression Construct
A simple example of Insert illustrating the target table and the VALUES clause at once:

>>> from sqlalchemy import insert
>>> stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")

The above stmt variable is an instance of Insert. Most SQL expressions can be stringified in place as a means to see the general form of what’s being produced:

>>> print(stmt)
INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)

The stringified form is created by producing a Compiled form of the object which includes a database-specific string SQL representation of the statement; we can acquire this object directly using the ClauseElement.compile() method:

>>> compiled = stmt.compile()

Our Insert construct is an example of a “parameterized” construct, illustrated previously at Sending Parameters; to view the name and fullname bound parameters, these are available from the Compiled construct as well:

>>> compiled.params
{'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}