## ORM-enabled UPDATE statements
As previously mentioned, there’s a second way to emit UPDATE statements in terms of the ORM, which is known as an ORM enabled UPDATE statement. This allows the use of a generic SQL UPDATE statement that can affect many rows at once. For example to emit an UPDATE that will change the User.fullname column based on a value in the User.name column:

>>> session.execute(
...     update(User)
...     .where(User.name == "sandy")
...     .values(fullname="Sandy Squirrel Extraordinaire")
... )
UPDATE user_account SET fullname=? WHERE user_account.name = ?
[...] ('Sandy Squirrel Extraordinaire', 'sandy')
<sqlalchemy.engine.cursor.CursorResult object ...>

When invoking the ORM-enabled UPDATE statement, special logic is used to locate objects in the current session that match the given criteria, so that they are refreshed with the new data. Above, the sandy object identity was located in memory and refreshed:

>>> sandy.fullname
'Sandy Squirrel Extraordinaire'

The refresh logic is known as the synchronize_session option, and is described in detail in the section UPDATE and DELETE with arbitrary WHERE clause.

