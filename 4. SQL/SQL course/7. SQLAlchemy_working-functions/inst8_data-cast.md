## Data Casts and Type Coercion
In SQL, we often need to indicate the datatype of an expression explicitly, either to tell the database what type is expected in an otherwise ambiguous expression, or in some cases when we want to convert the implied datatype of a SQL expression into something else. The SQL CAST keyword is used for this task, which in SQLAlchemy is provided by the cast() function. This function accepts a column expression and a data type object as arguments, as demonstrated below where we produce a SQL expression CAST(user_account.id AS VARCHAR) from the user_table.c.id column object:

>>> from sqlalchemy import cast
>>> stmt = select(cast(user_table.c.id, String))
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     result.all()
BEGIN (implicit)
SELECT CAST(user_account.id AS VARCHAR) AS id
FROM user_account
[...] ()
[('1',), ('2',), ('3',)]
ROLLBACK

The cast() function not only renders the SQL CAST syntax, it also produces a SQLAlchemy column expression that will act as the given datatype on the Python side as well. A string expression that is cast() to JSON will gain JSON subscript and comparison operators, for example:

>>> from sqlalchemy import JSON
>>> print(cast("{'a': 'b'}", JSON)["a"])
CAST(:param_1 AS JSON)[:param_2]