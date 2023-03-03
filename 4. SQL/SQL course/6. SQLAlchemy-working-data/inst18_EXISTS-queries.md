## EXISTS subqueries
The SQL EXISTS keyword is an operator that is used with scalar subqueries to return a boolean true or false depending on if the SELECT statement would return a row. SQLAlchemy includes a variant of the ScalarSelect object called Exists, which will generate an EXISTS subquery and is most conveniently generated using the SelectBase.exists() method. Below we produce an EXISTS so that we can return user_account rows that have more than one related row in address:

>>> subq = (
...     select(func.count(address_table.c.id))
...     .where(user_table.c.id == address_table.c.user_id)
...     .group_by(address_table.c.user_id)
...     .having(func.count(address_table.c.id) > 1)
... ).exists()
>>> with engine.connect() as conn:
...     result = conn.execute(select(user_table.c.name).where(subq))
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name
FROM user_account
WHERE EXISTS (SELECT count(address.id) AS count_1
FROM address
WHERE user_account.id = address.user_id GROUP BY address.user_id
HAVING count(address.id) > ?)
[...] (1,)
[('sandy',)]
ROLLBACK

The EXISTS construct is more often than not used as a negation, e.g. NOT EXISTS, as it provides a SQL-efficient form of locating rows for which a related table has no rows. Below we select user names that have no email addresses; note the binary negation operator (~) used inside the second WHERE clause:

>>> subq = (
...     select(address_table.c.id).where(user_table.c.id == address_table.c.user_id)
... ).exists()
>>> with engine.connect() as conn:
...     result = conn.execute(select(user_table.c.name).where(~subq))
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name
FROM user_account
WHERE NOT (EXISTS (SELECT address.id
FROM address
WHERE user_account.id = address.user_id))
[...] ()
[('patrick',)]
ROLLBACK