## Executing with an ORM Session

As mentioned previously, most of the patterns and examples above apply to use with the ORM as well, so here we will introduce this usage so that as the tutorial proceeds, we will be able to illustrate each pattern in terms of Core and ORM use together.

The fundamental transactional / database interactive object when using the ORM is called the Session. In modern SQLAlchemy, this object is used in a manner very similar to that of the Connection, and in fact as the Session is used, it refers to a Connection internally which it uses to emit SQL.

When the Session is used with non-ORM constructs, it passes through the SQL statements we give it and does not generally do things much differently from how the Connection does directly, so we can illustrate it here in terms of the simple textual SQL operations we’ve already learned.

The Session has a few different creational patterns, but here we will illustrate the most basic one that tracks exactly with how the Connection is used which is to construct it within a context manager:

>>> from sqlalchemy.orm import Session

>>> stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
>>> with Session(engine) as session:
...     result = session.execute(stmt, {"y": 6})
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table WHERE y > ? ORDER BY x, y
[...] (6,)
x: 6  y: 8
x: 9  y: 10
x: 11  y: 12
x: 13  y: 14
ROLLBACK

The example above can be compared to the example in the preceding section in Sending Parameters - we directly replace the call to with engine.connect() as conn with with Session(engine) as session, and then make use of the Session.execute() method just like we do with the Connection.execute() method.

Also, like the Connection, the Session features “commit as you go” behavior using the Session.commit() method, illustrated below using a textual UPDATE statement to alter some of our data:

>>> with Session(engine) as session:
...     result = session.execute(
...         text("UPDATE some_table SET y=:y WHERE x=:x"),
...         [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
...     )
...     session.commit()
BEGIN (implicit)
UPDATE some_table SET y=? WHERE x=?
[...] ((11, 9), (15, 13))
COMMIT

Above, we invoked an UPDATE statement using the bound-parameter, “executemany” style of execution introduced at Sending Multiple Parameters, ending the block with a “commit as you go” commit.

Tip

The Session doesn’t actually hold onto the Connection object after it ends the transaction. It gets a new Connection from the Engine the next time it needs to execute SQL against the database.

The Session obviously has a lot more tricks up its sleeve than that, however understanding that it has a Session.execute() method that’s used the same way as Connection.execute() will get us started with the examples that follow later.