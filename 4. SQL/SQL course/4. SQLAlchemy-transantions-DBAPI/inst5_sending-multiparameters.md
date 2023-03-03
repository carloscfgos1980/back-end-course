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