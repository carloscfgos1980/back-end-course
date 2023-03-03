## UPDATE..FROM
Some databases such as PostgreSQL and MySQL support a syntax “UPDATE FROM” where additional tables may be stated directly in a special FROM clause. This syntax will be generated implicitly when additional tables are located in the WHERE clause of the statement:

>>> update_stmt = (
...     update(user_table)
...     .where(user_table.c.id == address_table.c.user_id)
...     .where(address_table.c.email_address == "patrick@aol.com")
...     .values(fullname="Pat")
... )
>>> print(update_stmt)
UPDATE user_account SET fullname=:fullname FROM address
WHERE user_account.id = address.user_id AND address.email_address = :email_address_1

There is also a MySQL specific syntax that can UPDATE multiple tables. This requires we refer to Table objects in the VALUES clause in order to refer to additional tables:

>>> update_stmt = (
...     update(user_table)
...     .where(user_table.c.id == address_table.c.user_id)
...     .where(address_table.c.email_address == "patrick@aol.com")
...     .values(
...         {user_table.c.fullname: "Pat", address_table.c.email_address: "pat@aol.com"}
...     )
... )
>>> from sqlalchemy.dialects import mysql
>>> print(update_stmt.compile(dialect=mysql.dialect()))
UPDATE user_account, address
SET address.email_address=%s, user_account.fullname=%s
WHERE user_account.id = address.user_id AND address.email_address = %s