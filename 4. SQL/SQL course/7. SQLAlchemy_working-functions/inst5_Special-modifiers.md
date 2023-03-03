## Special Modifiers WITHIN GROUP, FILTER
The “WITHIN GROUP” SQL syntax is used in conjunction with an “ordered set” or a “hypothetical set” aggregate function. Common “ordered set” functions include percentile_cont() and rank(). SQLAlchemy includes built in implementations rank, dense_rank, mode, percentile_cont and percentile_disc which include a FunctionElement.within_group() method:

>>> print(
...     func.unnest(
...         func.percentile_disc([0.25, 0.5, 0.75, 1]).within_group(user_table.c.name)
...     )
... )
unnest(percentile_disc(:percentile_disc_1) WITHIN GROUP (ORDER BY user_account.name))

“FILTER” is supported by some backends to limit the range of an aggregate function to a particular subset of rows compared to the total range of rows returned, available using the FunctionElement.filter() method:

>>> stmt = (
...     select(
...         func.count(address_table.c.email_address).filter(user_table.c.name == "sandy"),
...         func.count(address_table.c.email_address).filter(
...             user_table.c.name == "spongebob"
...         ),
...     )
...     .select_from(user_table)
...     .join(address_table)
... )
>>> with engine.connect() as conn:  
...     result = conn.execute(stmt)
...     print(result.all())
BEGIN (implicit)
SELECT count(address.email_address) FILTER (WHERE user_account.name = ?) AS anon_1,
count(address.email_address) FILTER (WHERE user_account.name = ?) AS anon_2
FROM user_account JOIN address ON user_account.id = address.user_id
[...] ('sandy', 'spongebob')
[(2, 1)]
ROLLBACK