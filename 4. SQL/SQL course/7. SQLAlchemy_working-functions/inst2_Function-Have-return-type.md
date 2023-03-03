## Functions Have Return Types
As functions are column expressions, they also have SQL datatypes that describe the data type of a generated SQL expression. We refer to these types here as “SQL return types”, in reference to the type of SQL value that is returned by the function in the context of a database-side SQL expression, as opposed to the “return type” of a Python function.

The SQL return type of any SQL function may be accessed, typically for debugging purposes, by referring to the Function.type attribute:

>>> func.now().type
DateTime()

These SQL return types are significant when making use of the function expression in the context of a larger expression; that is, math operators will work better when the datatype of the expression is something like Integer or Numeric, JSON accessors in order to work need to be using a type such as JSON. Certain classes of functions return entire rows instead of column values, where there is a need to refer to specific columns; such functions are referred towards as table valued functions.

The SQL return type of the function may also be significant when executing a statement and getting rows back, for those cases where SQLAlchemy has to apply result-set processing. A prime example of this are date-related functions on SQLite, where SQLAlchemy’s DateTime and related datatypes take on the role of converting from string values to Python datetime() objects as result rows are received.

To apply a specific type to a function we’re creating, we pass it using the Function.type_ parameter; the type argument may be either a TypeEngine class or an instance. In the example below we pass the JSON class to generate the PostgreSQL json_object() function, noting that the SQL return type will be of type JSON:

>>> from sqlalchemy import JSON
>>> function_expr = func.json_object('{a, 1, b, "def", c, 3.5}', type_=JSON)

By creating our JSON function with the JSON datatype, the SQL expression object takes on JSON-related features, such as that of accessing elements:

>>> stmt = select(function_expr["def"])
>>> print(stmt)
SELECT json_object(:json_object_1)[:json_object_2] AS anon_1