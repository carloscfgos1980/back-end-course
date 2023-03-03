## Using RETURNING with UPDATE, DELETE
Like the Insert construct, Update and Delete also support the RETURNING clause which is added by using the Update.returning() and Delete.returning() methods. When these methods are used on a backend that supports RETURNING, selected columns from all rows that match the WHERE criteria of the statement will be returned in the Result object as rows that can be iterated:

>>> update_stmt = (
...     update(user_table)
...     .where(user_table.c.name == "patrick")
...     .values(fullname="Patrick the Star")
...     .returning(user_table.c.id, user_table.c.name)
... )
>>> print(update_stmt)
UPDATE user_account SET fullname=:fullname
WHERE user_account.name = :name_1
RETURNING user_account.id, user_account.name
>>> delete_stmt = (
...     delete(user_table)
...     .where(user_table.c.name == "patrick")
...     .returning(user_table.c.id, user_table.c.name)
... )
>>> print(delete_stmt)
DELETE FROM user_account
WHERE user_account.name = :name_1
RETURNING user_account.id, user_account.name