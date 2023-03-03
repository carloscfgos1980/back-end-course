with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table
[...] ()
x: 1  y: 1
x: 2  y: 4
x: 6  y: 8
x: 9  y: 10
ROLLBACK

'''<uple Assignment> - This is the most Python-idiomatic style, which is to assign variables to each row positionally as they are received:'''
result = conn.execute(text("select x, y from some_table"))

for x, y in result:
    # ...




'''<integer Index> - Tuples are Python sequences, so regular integer access is available too:'''
result = conn.execute(text("select x, y from some_table"))

  for row in result:
      x = row[0]



'''<Attribute Name> - As these are Python named tuples, the tuples have dynamic attribute names matching the names of each column. These names are normally the names that the SQL statement assigns to the columns in each row. While they are usually fairly predictable and can also be controlled by labels, in less defined cases they may be subject to database-specific behaviors:'''
result = conn.execute(text("select x, y from some_table"))

for row in result:
    y = row.y

    # illustrate use with Python f-strings
    print(f"Row: {row.x} {y}")



'''<Mapping Access> - To receive rows as Python mapping objects, which is essentially a read-only version of Python’s interface to the common dict object, the Result may be transformed into a MappingResult object using the Result.mappings() modifier; this is a result object that yields dictionary-like RowMapping objects rather than Row objects:'''

result = conn.execute(text("select x, y from some_table"))

for dict_row in result.mappings():
    x = dict_row["x"]
    y = dict_row["y"]

