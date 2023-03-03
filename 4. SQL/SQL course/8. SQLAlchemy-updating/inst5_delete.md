## The delete() SQL Expression Construct
The delete() function generates a new instance of Delete which represents a DELETE statement in SQL, that will delete rows from a table.

The delete() statement from an API perspective is very similar to that of the update() construct, traditionally returning no rows but allowing for a RETURNING variant on some database backends.

>>> from sqlalchemy import delete
>>> stmt = delete(user_table).where(user_table.c.name == "patrick")
>>> print(stmt)
DELETE FROM user_account WHERE user_account.name = :name_1

## Multiple Table Deletes
Like Update, Delete supports the use of correlated subqueries in the WHERE clause as well as backend-specific multiple table syntaxes, such as DELETE FROM..USING on MySQL:

>>> delete_stmt = (
...     delete(user_table)
...     .where(user_table.c.id == address_table.c.user_id)
...     .where(address_table.c.email_address == "patrick@aol.com")
... )
>>> from sqlalchemy.dialects import mysql
>>> print(delete_stmt.compile(dialect=mysql.dialect()))
DELETE FROM user_account USING user_account, address
WHERE user_account.id = address.user_id AND address.email_address = %s