## Working with SQL Functions
First introduced earlier in this section at Aggregate functions with GROUP BY / HAVING, the func object serves as a factory for creating new Function objects, which when used in a construct like select(), produce a SQL function display, typically consisting of a name, some parenthesis (although not always), and possibly some arguments. Examples of typical SQL functions include:

the count() function, an aggregate function which counts how many rows are returned:

>>> print(select(func.count()).select_from(user_table))
SELECT count(*) AS count_1
FROM user_account

the lower() function, a string function that converts a string to lower case:

>>> print(select(func.lower("A String With Much UPPERCASE")))
SELECT lower(:lower_2) AS lower_1

the now() function, which provides for the current date and time; as this is a common function, SQLAlchemy knows how to render this differently for each backend, in the case of SQLite using the CURRENT_TIMESTAMP function:

>>> stmt = select(func.now())
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     print(result.all())
BEGIN (implicit)
SELECT CURRENT_TIMESTAMP AS now_1
[...] ()
[(datetime.datetime(...),)]
ROLLBACK

As most database backends feature dozens if not hundreds of different SQL functions, func tries to be as liberal as possible in what it accepts. Any name that is accessed from this namespace is automatically considered to be a SQL function that will render in a generic way:

>>> print(select(func.some_crazy_function(user_table.c.name, 17)))
SELECT some_crazy_function(user_account.name, :some_crazy_function_2) AS some_crazy_function_1
FROM user_account

At the same time, a relatively small set of extremely common SQL functions such as count, now, max, concat include pre-packaged versions of themselves which provide for proper typing information as well as backend-specific SQL generation in some cases. The example below contrasts the SQL generation that occurs for the PostgreSQL dialect compared to the Oracle dialect for the now function:

>>> from sqlalchemy.dialects import postgresql
>>> print(select(func.now()).compile(dialect=postgresql.dialect()))
SELECT now() AS now_1

>>> from sqlalchemy.dialects import oracle
>>> print(select(func.now()).compile(dialect=oracle.dialect()))
SELECT CURRENT_TIMESTAMP AS now_1 FROM DUAL