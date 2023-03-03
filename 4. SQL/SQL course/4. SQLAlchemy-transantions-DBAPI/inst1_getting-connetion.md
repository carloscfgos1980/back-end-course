## Working with Transactions and the DBAPI
With the Engine object ready to go, we may now proceed to dive into the basic operation of an Engine and its primary interactive endpoints, the Connection and Result. We will additionally introduce the ORM’s facade for these objects, known as the Session.

Note to ORM readers

When using the ORM, the Engine is managed by another object called the Session. The Session in modern SQLAlchemy emphasizes a transactional and SQL execution pattern that is largely identical to that of the Connection discussed below, so while this subsection is Core-centric, all of the concepts here are essentially relevant to ORM use as well and is recommended for all ORM learners. The execution pattern used by the Connection will be contrasted with that of the Session at the end of this section.

As we have yet to introduce the SQLAlchemy Expression Language that is the primary feature of SQLAlchemy, we will make use of one simple construct within this package called the text() construct, which allows us to write SQL statements as textual SQL. Rest assured that textual SQL in day-to-day SQLAlchemy use is by far the exception rather than the rule for most tasks, even though it always remains fully available.

## Getting a Connection
The sole purpose of the Engine object from a user-facing perspective is to provide a unit of connectivity to the database called the Connection. When working with the Core directly, the Connection object is how all interaction with the database is done. As the Connection represents an open resource against the database, we want to always limit the scope of our use of this object to a specific context, and the best way to do that is by using Python context manager form, also known as the with statement. Below we illustrate “Hello World”, using a textual SQL statement. Textual SQL is emitted using a construct called text() that will be discussed in more detail later:

>>> from sqlalchemy import text

>>> with engine.connect() as conn:
...     result = conn.execute(text("select 'hello world'"))
...     print(result.all())
BEGIN (implicit)
select 'hello world'
[...] ()
[('hello world',)]
ROLLBACK

In the above example, the context manager provided for a database connection and also framed the operation inside of a transaction. The default behavior of the Python DBAPI includes that a transaction is always in progress; when the scope of the connection is released, a ROLLBACK is emitted to end the transaction. The transaction is not committed automatically; when we want to commit data we normally need to call Connection.commit() as we’ll see in the next section.

Tip

“autocommit” mode is available for special cases. The section Setting Transaction Isolation Levels including DBAPI Autocommit discusses this.

The result of our SELECT was also returned in an object called Result that will be discussed later, however for the moment we’ll add that it’s best to ensure this object is consumed within the “connect” block, and is not passed along outside of the scope of our connection.