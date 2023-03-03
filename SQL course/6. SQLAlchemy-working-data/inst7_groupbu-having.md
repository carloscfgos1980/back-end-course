## Aggregate functions with GROUP BY / HAVING
In SQL, aggregate functions allow column expressions across multiple rows to be aggregated together to produce a single result. Examples include counting, computing averages, as well as locating the maximum or minimum value in a set of values.

SQLAlchemy provides for SQL functions in an open-ended way using a namespace known as func. This is a special constructor object which will create new instances of Function when given the name of a particular SQL function, which can have any name, as well as zero or more arguments to pass to the function, which are, like in all other cases, SQL Expression constructs. For example, to render the SQL COUNT() function against the user_account.id column, we call upon the count() name:

>>> from sqlalchemy import func
>>> count_fn = func.count(user_table.c.id)
>>> print(count_fn)
count(user_account.id)

SQL functions are described in more detail later in this tutorial at Working with SQL Functions.

When using aggregate functions in SQL, the GROUP BY clause is essential in that it allows rows to be partitioned into groups where aggregate functions will be applied to each group individually. When requesting non-aggregated columns in the COLUMNS clause of a SELECT statement, SQL requires that these columns all be subject to a GROUP BY clause, either directly or indirectly based on a primary key association. The HAVING clause is then used in a similar manner as the WHERE clause, except that it filters out rows based on aggregated values rather than direct row contents.

SQLAlchemy provides for these two clauses using the Select.group_by() and Select.having() methods. Below we illustrate selecting user name fields as well as count of addresses, for those users that have more than one address:

>>> with engine.connect() as conn:
...     result = conn.execute(
...         select(User.name, func.count(Address.id).label("count"))
...         .join(Address)
...         .group_by(User.name)
...         .having(func.count(Address.id) > 1)
...     )
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name, count(address.id) AS count
FROM user_account JOIN address ON user_account.id = address.user_id GROUP BY user_account.name
HAVING count(address.id) > ?
[...] (1,)
[('sandy', 2)]
ROLLBACK