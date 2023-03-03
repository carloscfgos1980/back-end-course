## Setting the COLUMNS and FROM clause
The select() function accepts positional elements representing any number of Column and/or Table expressions, as well as a wide range of compatible objects, which are resolved into a list of SQL expressions to be SELECTed from that will be returned as columns in the result set. These elements also serve in simpler cases to create the FROM clause, which is inferred from the columns and table-like expressions passed:

>>> print(select(user_table))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account

To SELECT from individual columns using a Core approach, Column objects are accessed from the Table.c accessor and can be sent directly; the FROM clause will be inferred as the set of all Table and other FromClause objects that are represented by those columns:

>>> print(select(user_table.c.name, user_table.c.fullname))
SELECT user_account.name, user_account.fullname
FROM user_account

Selecting ORM Entities and Columns
ORM entities, such our User class as well as the column-mapped attributes upon it such as User.name, also participate in the SQL Expression Language system representing tables and columns. Below illustrates an example of SELECTing from the User entity, which ultimately renders in the same way as if we had used user_table directly:

>>> print(select(User))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account

When executing a statement like the above using the ORM Session.execute() method, there is an important difference when we select from a full entity such as User, as opposed to user_table, which is that the entity itself is returned as a single element within each row. That is, when we fetch rows from the above statement, as there is only the User entity in the list of things to fetch, we get back Row objects that have only one element, which contain instances of the User class:

>>> row = session.execute(select(User)).first()
BEGIN...
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
[...] ()
>>> row
(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)

The above Row has just one element, representing the User entity:

>>> row[0]
User(id=1, name='spongebob', fullname='Spongebob Squarepants')

A highly recommended convenience method of achieving the same result as above is to use the Session.scalars() method to execute the statement directly; this method will return a ScalarResult object that delivers the first “column” of each row at once, in this case, instances of the User class:

>>> user = session.scalars(select(User)).first()
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
[...] ()
>>> user
User(id=1, name='spongebob', fullname='Spongebob Squarepants')

Alternatively, we can select individual columns of an ORM entity as distinct elements within result rows, by using the class-bound attributes; when these are passed to a construct such as select(), they are resolved into the Column or other SQL expression represented by each attribute:

>>> print(select(User.name, User.fullname))
SELECT user_account.name, user_account.fullname
FROM user_account

When we invoke this statement using Session.execute(), we now receive rows that have individual elements per value, each corresponding to a separate column or other SQL expression:

>>> row = session.execute(select(User.name, User.fullname)).first()
SELECT user_account.name, user_account.fullname
FROM user_account
[...] ()
>>> row
('spongebob', 'Spongebob Squarepants')

The approaches can also be mixed, as below where we SELECT the name attribute of the User entity as the first element of the row, and combine it with full Address entities in the second element:

>>> session.execute(
...     select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
... ).all()
SELECT user_account.name, address.id, address.email_address, address.user_id
FROM user_account, address
WHERE user_account.id = address.user_id ORDER BY address.id
[...] ()
[('spongebob', Address(id=1, email_address='spongebob@sqlalchemy.org')),
('sandy', Address(id=2, email_address='sandy@sqlalchemy.org')),
('sandy', Address(id=3, email_address='sandy@squirrelpower.org'))]

Approaches towards selecting ORM entities and columns as well as common methods for converting rows are discussed further at Selecting ORM Entities and Attributes.

## Selecting from Labeled SQL Expressions
The ColumnElement.label() method as well as the same-named method available on ORM attributes provides a SQL label of a column or expression, allowing it to have a specific name in a result set. This can be helpful when referring to arbitrary SQL expressions in a result row by name:

>>> from sqlalchemy import func, cast
>>> stmt = select(
...     ("Username: " + user_table.c.name).label("username"),
... ).order_by(user_table.c.name)
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(f"{row.username}")
BEGIN (implicit)
SELECT ? || user_account.name AS username
FROM user_account ORDER BY user_account.name
[...] ('Username: ',)
Username: patrick
Username: sandy
Username: spongebob
ROLLBACK

## Selecting with Textual Column Expressions
When we construct a Select object using the select() function, we are normally passing to it a series of Table and Column objects that were defined using table metadata, or when using the ORM we may be sending ORM-mapped attributes that represent table columns. However, sometimes there is also the need to manufacture arbitrary SQL blocks inside of statements, such as constant string expressions, or just some arbitrary SQL that’s quicker to write literally.

The text() construct introduced at Working with Transactions and the DBAPI can in fact be embedded into a Select construct directly, such as below where we manufacture a hardcoded string literal 'some label' and embed it within the SELECT statement:

>>> from sqlalchemy import text
>>> stmt = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)
>>> with engine.connect() as conn:
...     print(conn.execute(stmt).all())
BEGIN (implicit)
SELECT 'some phrase', user_account.name
FROM user_account ORDER BY user_account.name
[generated in ...] ()
[('some phrase', 'patrick'), ('some phrase', 'sandy'), ('some phrase', 'spongebob')]
ROLLBACK

While the text() construct can be used in most places to inject literal SQL phrases, more often than not we are actually dealing with textual units that each represent an individual column expression. In this common case we can get more functionality out of our textual fragment using the literal_column() construct instead. This object is similar to text() except that instead of representing arbitrary SQL of any form, it explicitly represents a single “column” and can then be labeled and referred towards in subqueries and other expressions:

>>> from sqlalchemy import literal_column
>>> stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(
...     user_table.c.name
... )
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(f"{row.p}, {row.name}")
BEGIN (implicit)
SELECT 'some phrase' AS p, user_account.name
FROM user_account ORDER BY user_account.name
[generated in ...] ()
some phrase, patrick
some phrase, sandy
some phrase, spongebob
ROLLBACK

Note that in both cases, when using text() or literal_column(), we are writing a syntactical SQL expression, and not a literal value. We therefore have to include whatever quoting or syntaxes are necessary for the SQL we want to see rendered.


## The WHERE clause
SQLAlchemy allows us to compose SQL expressions, such as name = 'squidward' or user_id > 10, by making use of standard Python operators in conjunction with Column and similar objects. For boolean expressions, most Python operators such as ==, !=, <, >= etc. generate new SQL Expression objects, rather than plain boolean True/False values:

>>> print(user_table.c.name == "squidward")
user_account.name = :name_1

>>> print(address_table.c.user_id > 10)
address.user_id > :user_id_1

We can use expressions like these to generate the WHERE clause by passing the resulting objects to the Select.where() method:

>>> print(select(user_table).where(user_table.c.name == "squidward"))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1

To produce multiple expressions joined by AND, the Select.where() method may be invoked any number of times:

>>> print(
...     select(address_table.c.email_address)
...     .where(user_table.c.name == "squidward")
...     .where(address_table.c.user_id == user_table.c.id)
... )
SELECT address.email_address
FROM address, user_account
WHERE user_account.name = :name_1 AND address.user_id = user_account.id

A single call to Select.where() also accepts multiple expressions with the same effect:

>>> print(
...     select(address_table.c.email_address).where(
...         user_table.c.name == "squidward", address_table.c.user_id == user_table.c.id
...     )
... )
SELECT address.email_address
FROM address, user_account
WHERE user_account.name = :name_1 AND address.user_id = user_account.id

“AND” and “OR” conjunctions are both available directly using the and_() and or_() functions, illustrated below in terms of ORM entities:

>>> from sqlalchemy import and_, or_
>>> print(
...     select(Address.email_address).where(
...         and_(
...             or_(User.name == "squidward", User.name == "sandy"),
...             Address.user_id == User.id,
...         )
...     )
... )
SELECT address.email_address
FROM address, user_account
WHERE (user_account.name = :name_1 OR user_account.name = :name_2)
AND address.user_id = user_account.id

For simple “equality” comparisons against a single entity, there’s also a popular method known as Select.filter_by() which accepts keyword arguments that match to column keys or ORM attribute names. It will filter against the leftmost FROM clause or the last entity joined:

>>> print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1 AND user_account.fullname = :fullname_1