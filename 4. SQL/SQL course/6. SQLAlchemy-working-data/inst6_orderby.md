## ORDER BY, GROUP BY, HAVING
The SELECT SQL statement includes a clause called ORDER BY which is used to return the selected rows within a given ordering.

The GROUP BY clause is constructed similarly to the ORDER BY clause, and has the purpose of sub-dividing the selected rows into specific groups upon which aggregate functions may be invoked. The HAVING clause is usually used with GROUP BY and is of a similar form to the WHERE clause, except that it’s applied to the aggregated functions used within groups.

ORDER BY
The ORDER BY clause is constructed in terms of SQL Expression constructs typically based on Column or similar objects. The Select.order_by() method accepts one or more of these expressions positionally:

>>> print(select(user_table).order_by(user_table.c.name))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.name

Ascending / descending is available from the ColumnElement.asc() and ColumnElement.desc() modifiers, which are present from ORM-bound attributes as well:

>>> print(select(User).order_by(User.fullname.desc()))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.fullname DESC

The above statement will yield rows that are sorted by the user_account.fullname column in descending order.