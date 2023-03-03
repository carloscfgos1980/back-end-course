## Table-Valued Functions
Table-valued SQL functions support a scalar representation that contains named sub-elements. Often used for JSON and ARRAY-oriented functions as well as functions like generate_series(), the table-valued function is specified in the FROM clause, and is then referred towards as a table, or sometimes even as a column. Functions of this form are prominent within the PostgreSQL database, however some forms of table valued functions are also supported by SQLite, Oracle, and SQL Server.

See also

Table values, Table and Column valued functions, Row and Tuple objects - in the PostgreSQL documentation.

While many databases support table valued and other special forms, PostgreSQL tends to be where there is the most demand for these features. See this section for additional examples of PostgreSQL syntaxes as well as additional features.

SQLAlchemy provides the FunctionElement.table_valued() method as the basic “table valued function” construct, which will convert a func object into a FROM clause containing a series of named columns, based on string names passed positionally. This returns a TableValuedAlias object, which is a function-enabled Alias construct that may be used as any other FROM clause as introduced at Using Aliases. Below we illustrate the json_each() function, which while common on PostgreSQL is also supported by modern versions of SQLite:

>>> onetwothree = func.json_each('["one", "two", "three"]').table_valued("value")
>>> stmt = select(onetwothree).where(onetwothree.c.value.in_(["two", "three"]))
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     result.all()
BEGIN (implicit)
SELECT anon_1.value
FROM json_each(?) AS anon_1
WHERE anon_1.value IN (?, ?)
[...] ('["one", "two", "three"]', 'two', 'three')
[('two',), ('three',)]
ROLLBACK

Above, we used the json_each() JSON function supported by SQLite and PostgreSQL to generate a table valued expression with a single column referred towards as value, and then selected two of its three rows.