## Using Aliases
Now that we are selecting from multiple tables and using joins, we quickly run into the case where we need to refer to the same table multiple times in the FROM clause of a statement. We accomplish this using SQL aliases, which are a syntax that supplies an alternative name to a table or subquery from which it can be referred towards in the statement.

In the SQLAlchemy Expression Language, these “names” are instead represented by FromClause objects known as the Alias construct, which is constructed in Core using the FromClause.alias() method. An Alias construct is just like a Table construct in that it also has a namespace of Column objects within the Alias.c collection. The SELECT statement below for example returns all unique pairs of user names:

>>> user_alias_1 = user_table.alias()
>>> user_alias_2 = user_table.alias()
>>> print(
...     select(user_alias_1.c.name, user_alias_2.c.name).join_from(
...         user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id
...     )
... )
SELECT user_account_1.name, user_account_2.name AS name_1
FROM user_account AS user_account_1
JOIN user_account AS user_account_2 ON user_account_1.id > user_account_2.id