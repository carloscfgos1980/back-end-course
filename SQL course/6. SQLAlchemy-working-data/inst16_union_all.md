## UNION, UNION ALL and other set operations
In SQL,SELECT statements can be merged together using the UNION or UNION ALL SQL operation, which produces the set of all rows produced by one or more statements together. Other set operations such as INTERSECT [ALL] and EXCEPT [ALL] are also possible.

SQLAlchemy’s Select construct supports compositions of this nature using functions like union(), intersect() and except_(), and the “all” counterparts union_all(), intersect_all() and except_all(). These functions all accept an arbitrary number of sub-selectables, which are typically Select constructs but may also be an existing composition.

The construct produced by these functions is the CompoundSelect, which is used in the same manner as the Select construct, except that it has fewer methods. The CompoundSelect produced by union_all() for example may be invoked directly using Connection.execute():

>>> from sqlalchemy import union_all
>>> stmt1 = select(user_table).where(user_table.c.name == "sandy")
>>> stmt2 = select(user_table).where(user_table.c.name == "spongebob")
>>> u = union_all(stmt1, stmt2)
>>> with engine.connect() as conn:
...     result = conn.execute(u)
...     print(result.all())
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
UNION ALL SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[generated in ...] ('sandy', 'spongebob')
[(2, 'sandy', 'Sandy Cheeks'), (1, 'spongebob', 'Spongebob Squarepants')]
ROLLBACK

To use a CompoundSelect as a subquery, just like Select it provides a SelectBase.subquery() method which will produce a Subquery object with a FromClause.c collection that may be referred towards in an enclosing select():

>>> u_subq = u.subquery()
>>> stmt = (
...     select(u_subq.c.name, address_table.c.email_address)
...     .join_from(address_table, u_subq)
...     .order_by(u_subq.c.name, address_table.c.email_address)
... )
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     print(result.all())
BEGIN (implicit)
SELECT anon_1.name, address.email_address
FROM address JOIN
  (SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
  FROM user_account
  WHERE user_account.name = ?
UNION ALL
  SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
  FROM user_account
  WHERE user_account.name = ?)
AS anon_1 ON anon_1.id = address.user_id
ORDER BY anon_1.name, address.email_address
[generated in ...] ('sandy', 'spongebob')
[('sandy', 'sandy@sqlalchemy.org'), ('sandy', 'sandy@squirrelpower.org'), ('spongebob', 'spongebob@sqlalchemy.org')]
ROLLBACK