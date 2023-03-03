## Column Valued Functions - Table Valued Function as a Scalar Column
A special syntax supported by PostgreSQL and Oracle is that of referring towards a function in the FROM clause, which then delivers itself as a single column in the columns clause of a SELECT statement or other column expression context. PostgreSQL makes great use of this syntax for such functions as json_array_elements(), json_object_keys(), json_each_text(), json_each(), etc.

SQLAlchemy refers to this as a “column valued” function and is available by applying the FunctionElement.column_valued() modifier to a Function construct:

>>> from sqlalchemy import select, func
>>> stmt = select(func.json_array_elements('["one", "two"]').column_valued("x"))
>>> print(stmt)
SELECT x
FROM json_array_elements(:json_array_elements_1) AS x

The “column valued” form is also supported by the Oracle dialect, where it is usable for custom SQL functions:

>>> from sqlalchemy.dialects import oracle
>>> stmt = select(func.scalar_strings(5).column_valued("s"))
>>> print(stmt.compile(dialect=oracle.dialect()))
SELECT s.COLUMN_VALUE
FROM TABLE (scalar_strings(:scalar_strings_1)) s