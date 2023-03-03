## Updating and Deleting Rows with Core
So far we’ve covered Insert, so that we can get some data into our database, and then spent a lot of time on Select which handles the broad range of usage patterns used for retrieving data from the database. In this section we will cover the Update and Delete constructs, which are used to modify existing rows as well as delete existing rows. This section will cover these constructs from a Core-centric perspective.

ORM Readers - As was the case mentioned at Inserting Rows with Core, the Update and Delete operations when used with the ORM are usually invoked internally from the Session object as part of the unit of work process.

However, unlike Insert, the Update and Delete constructs can also be used directly with the ORM, using a pattern known as “ORM-enabled update and delete”; for this reason, familiarity with these constructs is useful for ORM use. Both styles of use are discussed in the sections Updating ORM Objects and Deleting ORM Objects.

The update() SQL Expression Construct
The update() function generates a new instance of Update which represents an UPDATE statement in SQL, that will update existing data in a table.

Like the insert() construct, there is a “traditional” form of update(), which emits UPDATE against a single table at a time and does not return any rows. However some backends support an UPDATE statement that may modify multiple tables at once, and the UPDATE statement also supports RETURNING such that columns contained in matched rows may be returned in the result set.

A basic UPDATE looks like:

>>> from sqlalchemy import update
>>> stmt = (
...     update(user_table)
...     .where(user_table.c.name == "patrick")
...     .values(fullname="Patrick the Star")
... )
>>> print(stmt)
UPDATE user_account SET fullname=:fullname WHERE user_account.name = :name_1

The Update.values() method controls the contents of the SET elements of the UPDATE statement. This is the same method shared by the Insert construct. Parameters can normally be passed using the column names as keyword arguments.

UPDATE supports all the major SQL forms of UPDATE, including updates against expressions, where we can make use of Column expressions:

>>> stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
>>> print(stmt)
UPDATE user_account SET fullname=(:name_1 || user_account.name)

To support UPDATE in an “executemany” context, where many parameter sets will be invoked against the same statement, the bindparam() construct may be used to set up bound parameters; these replace the places that literal values would normally go:

>>> from sqlalchemy import bindparam
>>> stmt = (
...     update(user_table)
...     .where(user_table.c.name == bindparam("oldname"))
...     .values(name=bindparam("newname"))
... )
>>> with engine.begin() as conn:
...     conn.execute(
...         stmt,
...         [
...             {"oldname": "jack", "newname": "ed"},
...             {"oldname": "wendy", "newname": "mary"},
...             {"oldname": "jim", "newname": "jake"},
...         ],
...     )
BEGIN (implicit)
UPDATE user_account SET name=? WHERE user_account.name = ?
[...] (('ed', 'jack'), ('mary', 'wendy'), ('jake', 'jim'))
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT

Other techniques which may be applied to UPDATE include: