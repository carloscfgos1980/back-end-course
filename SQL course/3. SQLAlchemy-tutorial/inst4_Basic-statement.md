## Basics of Statement Execution

We have seen a few examples that run SQL statements against a database, making use of a method called Connection.execute(), in conjunction with an object called text(), and returning an object called Result. In this section we’ll illustrate more closely the mechanics and interactions of these components.

Most of the content in this section applies equally well to modern ORM use when using the Session.execute() method, which works very similarly to that of Connection.execute(), including that ORM result rows are delivered using the same Result interface used by Core.

Fetching Rows
We’ll first illustrate the Result object more closely by making use of the rows we’ve inserted previously, running a textual SELECT statement on the table we’ve created:

>>> with engine.connect() as conn:
...     result = conn.execute(text("SELECT x, y FROM some_table"))
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table
[...] ()
x: 1  y: 1
x: 2  y: 4
x: 6  y: 8
x: 9  y: 10
ROLLBACK

Above, the “SELECT” string we executed selected all rows from our table. The object returned is called Result and represents an iterable object of result rows.

Result has lots of methods for fetching and transforming rows, such as the Result.all() method illustrated previously, which returns a list of all Row objects. It also implements the Python iterator interface so that we can iterate over the collection of Row objects directly.

The Row objects themselves are intended to act like Python named tuples. Below we illustrate a variety of ways to access rows.

Tuple Assignment - This is the most Python-idiomatic style, which is to assign variables to each row positionally as they are received:

result = conn.execute(text("select x, y from some_table"))

for x, y in result:
    # ...

Integer Index - Tuples are Python sequences, so regular integer access is available too:

result = conn.execute(text("select x, y from some_table"))

  for row in result:
      x = row[0]

Attribute Name - As these are Python named tuples, the tuples have dynamic attribute names matching the names of each column. These names are normally the names that the SQL statement assigns to the columns in each row. While they are usually fairly predictable and can also be controlled by labels, in less defined cases they may be subject to database-specific behaviors:

result = conn.execute(text("select x, y from some_table"))

for row in result:
    y = row.y

    # illustrate use with Python f-strings
    print(f"Row: {row.x} {y}")

Mapping Access - To receive rows as Python mapping objects, which is essentially a read-only version of Python’s interface to the common dict object, the Result may be transformed into a MappingResult object using the Result.mappings() modifier; this is a result object that yields dictionary-like RowMapping objects rather than Row objects:

result = conn.execute(text("select x, y from some_table"))

for dict_row in result.mappings():
    x = dict_row["x"]
    y = dict_row["y"]