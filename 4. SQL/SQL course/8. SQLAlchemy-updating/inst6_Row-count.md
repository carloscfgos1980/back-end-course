## Getting Affected Row Count from UPDATE, DELETE
Both Update and Delete support the ability to return the number of rows matched after the statement proceeds, for statements that are invoked using Core Connection, i.e. Connection.execute(). Per the caveats mentioned below, this value is available from the CursorResult.rowcount attribute:

>>> with engine.begin() as conn:
...     result = conn.execute(
...         update(user_table)
...         .values(fullname="Patrick McStar")
...         .where(user_table.c.name == "patrick")
...     )
...     print(result.rowcount)
BEGIN (implicit)
UPDATE user_account SET fullname=? WHERE user_account.name = ?
[...] ('Patrick McStar', 'patrick')
1
COMMIT

Tip

The CursorResult class is a subclass of Result which contains additional attributes that are specific to the DBAPI cursor object. An instance of this subclass is returned when a statement is invoked via the Connection.execute() method. When using the ORM, the Session.execute() method returns an object of this type for all INSERT, UPDATE, and DELETE statements.

Facts about CursorResult.rowcount:

The value returned is the number of rows matched by the WHERE clause of the statement. It does not matter if the row were actually modified or not.

CursorResult.rowcount is not necessarily available for an UPDATE or DELETE statement that uses RETURNING.

For an executemany execution, CursorResult.rowcount may not be available either, which depends highly on the DBAPI module in use as well as configured options. The attribute CursorResult.supports_sane_multi_rowcount indicates if this value will be available for the current backend in use.

Some drivers, particularly third party dialects for non-relational databases, may not support CursorResult.rowcount at all. The CursorResult.supports_sane_rowcount will indicate this.

“rowcount” is used by the ORM unit of work process to validate that an UPDATE or DELETE statement matched the expected number of rows, and is also essential for the ORM versioning feature documented at Configuring a Version Counter.