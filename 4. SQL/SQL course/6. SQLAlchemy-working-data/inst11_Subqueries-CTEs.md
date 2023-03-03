## Subqueries and CTEs
A subquery in SQL is a SELECT statement that is rendered within parenthesis and placed within the context of an enclosing statement, typically a SELECT statement but not necessarily.

This section will cover a so-called “non-scalar” subquery, which is typically placed in the FROM clause of an enclosing SELECT. We will also cover the Common Table Expression or CTE, which is used in a similar way as a subquery, but includes additional features.

SQLAlchemy uses the Subquery object to represent a subquery and the CTE to represent a CTE, usually obtained from the Select.subquery() and Select.cte() methods, respectively. Either object can be used as a FROM element inside of a larger select() construct.

We can construct a Subquery that will select an aggregate count of rows from the address table (aggregate functions and GROUP BY were introduced previously at Aggregate functions with GROUP BY / HAVING):

>>> subq = (
...     select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
...     .group_by(address_table.c.user_id)
...     .subquery()
... )

Stringifying the subquery by itself without it being embedded inside of another Select or other statement produces the plain SELECT statement without any enclosing parenthesis:

>>> print(subq)
SELECT count(address.id) AS count, address.user_id
FROM address GROUP BY address.user_id

The Subquery object behaves like any other FROM object such as a Table, notably that it includes a Subquery.c namespace of the columns which it selects. We can use this namespace to refer to both the user_id column as well as our custom labeled count expression:

>>> print(select(subq.c.user_id, subq.c.count))
SELECT anon_1.user_id, anon_1.count
FROM (SELECT count(address.id) AS count, address.user_id AS user_id
FROM address GROUP BY address.user_id) AS anon_1

With a selection of rows contained within the subq object, we can apply the object to a larger Select that will join the data to the user_account table:

>>> stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
...     user_table, subq
... )

>>> print(stmt)
SELECT user_account.name, user_account.fullname, anon_1.count
FROM user_account JOIN (SELECT count(address.id) AS count, address.user_id AS user_id
FROM address GROUP BY address.user_id) AS anon_1 ON user_account.id = anon_1.user_id

In order to join from user_account to address, we made use of the Select.join_from() method. As has been illustrated previously, the ON clause of this join was again inferred based on foreign key constraints. Even though a SQL subquery does not itself have any constraints, SQLAlchemy can act upon constraints represented on the columns by determining that the subq.c.user_id column is derived from the address_table.c.user_id column, which does express a foreign key relationship back to the user_table.c.id column which is then used to generate the ON clause.