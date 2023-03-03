## Sending Parameters

SQL statements are usually accompanied by data that is to be passed with the statement itself, as we saw in the INSERT example previously. The Connection.execute() method therefore also accepts parameters, which are referred towards as bound parameters. A rudimentary example might be if we wanted to limit our SELECT statement only to rows that meet a certain criteria, such as rows where the “y” value were greater than a certain value that is passed in to a function.

In order to achieve this such that the SQL statement can remain fixed and that the driver can properly sanitize the value, we add a WHERE criteria to our statement that names a new parameter called “y”; the text() construct accepts these using a colon format “:y”. The actual value for “:y” is then passed as the second argument to Connection.execute() in the form of a dictionary:

>>> with engine.connect() as conn:
...     result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table WHERE y > ?
[...] (2,)
x: 2  y: 4
x: 6  y: 8
x: 9  y: 10
ROLLBACK

In the logged SQL output, we can see that the bound parameter :y was converted into a question mark when it was sent to the SQLite database. This is because the SQLite database driver uses a format called “qmark parameter style”, which is one of six different formats allowed by the DBAPI specification. SQLAlchemy abstracts these formats into just one, which is the “named” format using a colon.

Always use bound parameters

As mentioned at the beginning of this section, textual SQL is not the usual way we work with SQLAlchemy. However, when using textual SQL, a Python literal value, even non-strings like integers or dates, should never be stringified into SQL string directly; a parameter should always be used. This is most famously known as how to avoid SQL injection attacks when the data is untrusted. However it also allows the SQLAlchemy dialects and/or DBAPI to correctly handle the incoming input for the backend. Outside of plain textual SQL use cases, SQLAlchemy’s Core Expression API otherwise ensures that Python literal values are passed as bound parameters where appropriate.

## Sending Multiple Parameters
In the example at Committing Changes, we executed an INSERT statement where it appeared that we were able to INSERT multiple rows into the database at once. For statements that operate upon data, but do not return result sets, namely DML statements such as “INSERT” which don’t include a phrase like “RETURNING”, we can send multi params to the Connection.execute() method by passing a list of dictionaries instead of a single dictionary, thus allowing the single SQL statement to be invoked against each parameter set individually:

>>> with engine.connect() as conn:
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
...     )
...     conn.commit()
BEGIN (implicit)
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] ((11, 12), (13, 14))
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT

Behind the scenes, the Connection objects uses a DBAPI feature known as cursor.executemany(). This method performs the equivalent operation of invoking the given SQL statement against each parameter set individually. The DBAPI may optimize this operation in a variety of ways, by using prepared statements, or by concatenating the parameter sets into a single SQL statement in some cases. Some SQLAlchemy dialects may also use alternate APIs for this case, such as the psycopg2 dialect for PostgreSQL which uses more performant APIs for this use case.

Tip

you may have noticed this section isn’t tagged as an ORM concept. That’s because the “multiple parameters” use case is usually used for INSERT statements, which when using the ORM are invoked in a different way. Multiple parameters also may be used with UPDATE and DELETE statements to emit distinct UPDATE/DELETE operations on a per-row basis, however again when using the ORM, there is a different technique generally used for updating or deleting many individual rows separately.