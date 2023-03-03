## Common Table Expressions (CTEs)
Usage of the CTE construct in SQLAlchemy is virtually the same as how the Subquery construct is used. By changing the invocation of the Select.subquery() method to use Select.cte() instead, we can use the resulting object as a FROM element in the same way, but the SQL rendered is the very different common table expression syntax:

>>> subq = (
...     select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
...     .group_by(address_table.c.user_id)
...     .cte()
... )

>>> stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
...     user_table, subq
... )

>>> print(stmt)
WITH anon_1 AS
(SELECT count(address.id) AS count, address.user_id AS user_id
FROM address GROUP BY address.user_id)
 SELECT user_account.name, user_account.fullname, anon_1.count
FROM user_account JOIN anon_1 ON user_account.id = anon_1.user_id

The CTE construct also features the ability to be used in a “recursive” style, and may in more elaborate cases be composed from the RETURNING clause of an INSERT, UPDATE or DELETE statement. The docstring for CTE includes details on these additional patterns.

In both cases, the subquery and CTE were named at the SQL level using an “anonymous” name. In the Python code, we don’t need to provide these names at all. The object identity of the Subquery or CTE instances serves as the syntactical identity of the object when rendered. A name that will be rendered in the SQL can be provided by passing it as the first argument of the Select.subquery() or Select.cte() methods.