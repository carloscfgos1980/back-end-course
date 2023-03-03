## Executing the Statement
Invoking the statement we can INSERT a row into user_table. The INSERT SQL as well as the bundled parameters can be seen in the SQL logging:

>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     conn.commit()
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('spongebob', 'Spongebob Squarepants')
COMMIT

In its simple form above, the INSERT statement does not return any rows, and if only a single row is inserted, it will usually include the ability to return information about column-level default values that were generated during the INSERT of that row, most commonly an integer primary key value. In the above case the first row in a SQLite database will normally return 1 for the first integer primary key value, which we can acquire using the CursorResult.inserted_primary_key accessor:

>>> result.inserted_primary_key
(1,)

Tip

CursorResult.inserted_primary_key returns a tuple because a primary key may contain multiple columns. This is known as a composite primary key. The CursorResult.inserted_primary_key is intended to always contain the complete primary key of the record just inserted, not just a “cursor.lastrowid” kind of value, and is also intended to be populated regardless of whether or not “autoincrement” were used, hence to express a complete primary key it’s a tuple.