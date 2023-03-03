## Scalar and Correlated Subqueries
A scalar subquery is a subquery that returns exactly zero or one row and exactly one column. The subquery is then used in the COLUMNS or WHERE clause of an enclosing SELECT statement and is different than a regular subquery in that it is not used in the FROM clause. A correlated subquery is a scalar subquery that refers to a table in the enclosing SELECT statement.

SQLAlchemy represents the scalar subquery using the ScalarSelect construct, which is part of the ColumnElement expression hierarchy, in contrast to the regular subquery which is represented by the Subquery construct, which is in the FromClause hierarchy.

Scalar subqueries are often, but not necessarily, used with aggregate functions, introduced previously at Aggregate functions with GROUP BY / HAVING. A scalar subquery is indicated explicitly by making use of the Select.scalar_subquery() method as below. It’s default string form when stringified by itself renders as an ordinary SELECT statement that is selecting from two tables:

>>> subq = (
...     select(func.count(address_table.c.id))
...     .where(user_table.c.id == address_table.c.user_id)
...     .scalar_subquery()
... )
>>> print(subq)
(SELECT count(address.id) AS count_1
FROM address, user_account
WHERE user_account.id = address.user_id)

The above subq object now falls within the ColumnElement SQL expression hierarchy, in that it may be used like any other column expression:

>>> print(subq == 5)
(SELECT count(address.id) AS count_1
FROM address, user_account
WHERE user_account.id = address.user_id) = :param_1

Although the scalar subquery by itself renders both user_account and address in its FROM clause when stringified by itself, when embedding it into an enclosing select() construct that deals with the user_account table, the user_account table is automatically correlated, meaning it does not render in the FROM clause of the subquery:

>>> stmt = select(user_table.c.name, subq.label("address_count"))
>>> print(stmt)
SELECT user_account.name, (SELECT count(address.id) AS count_1
FROM address
WHERE user_account.id = address.user_id) AS address_count
FROM user_account

Simple correlated subqueries will usually do the right thing that’s desired. However, in the case where the correlation is ambiguous, SQLAlchemy will let us know that more clarity is needed:

>>> stmt = (
...     select(
...         user_table.c.name, address_table.c.email_address, subq.label("address_count")
...     )
...     .join_from(user_table, address_table)
...     .order_by(user_table.c.id, address_table.c.id)
... )
>>> print(stmt)
Traceback (most recent call last):
...
InvalidRequestError: Select statement '<... Select object at ...>' returned
no FROM clauses due to auto-correlation; specify correlate(<tables>) to
control correlation manually.

To specify that the user_table is the one we seek to correlate we specify this using the ScalarSelect.correlate() or ScalarSelect.correlate_except() methods:

>>> subq = (
...     select(func.count(address_table.c.id))
...     .where(user_table.c.id == address_table.c.user_id)
...     .scalar_subquery()
...     .correlate(user_table)
... )

The statement then can return the data for this column like any other:

>>> with engine.connect() as conn:
...     result = conn.execute(
...         select(
...             user_table.c.name,
...             address_table.c.email_address,
...             subq.label("address_count"),
...         )
...         .join_from(user_table, address_table)
...         .order_by(user_table.c.id, address_table.c.id)
...     )
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name, address.email_address, (SELECT count(address.id) AS count_1
FROM address
WHERE user_account.id = address.user_id) AS address_count
FROM user_account JOIN address ON user_account.id = address.user_id ORDER BY user_account.id, address.id
[...] ()
[('spongebob', 'spongebob@sqlalchemy.org', 1), ('sandy', 'sandy@sqlalchemy.org', 2),
 ('sandy', 'sandy@squirrelpower.org', 2)]
ROLLBACK