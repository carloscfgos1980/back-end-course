## Built-in Functions Have Pre-Configured Return Types
For common aggregate functions like count, max, min as well as a very small number of date functions like now and string functions like concat, the SQL return type is set up appropriately, sometimes based on usage. The max function and similar aggregate filtering functions will set up the SQL return type based on the argument given:

>>> m1 = func.max(Column("some_int", Integer))
>>> m1.type
Integer()

>>> m2 = func.max(Column("some_str", String))
>>> m2.type
String()

Date and time functions typically correspond to SQL expressions described by DateTime, Date or Time:

>>> func.now().type
DateTime()
>>> func.current_date().type
Date()

A known string function such as concat will know that a SQL expression would be of type String:

>>> func.concat("x", "y").type
String()

However, for the vast majority of SQL functions, SQLAlchemy does not have them explicitly present in its very small list of known functions. For example, while there is typically no issue using SQL functions func.lower() and func.upper() to convert the casing of strings, SQLAlchemy doesn’t actually know about these functions, so they have a “null” SQL return type:

>>> func.upper("lowercase").type
NullType()

For simple functions like upper and lower, the issue is not usually significant, as string values may be received from the database without any special type handling on the SQLAlchemy side, and SQLAlchemy’s type coercion rules can often correctly guess intent as well; the Python + operator for example will be correctly interpreted as the string concatenation operator based on looking at both sides of the expression:

>>> print(select(func.upper("lowercase") + " suffix"))
SELECT upper(:upper_1) || :upper_2 AS anon_1

Overall, the scenario where the Function.type_ parameter is likely necessary is:

the function is not already a SQLAlchemy built-in function; this can be evidenced by creating the function and observing the Function.type attribute, that is:

>>> func.count().type
Integer()

vs.:

>>> func.json_object('{"a", "b"}').type
NullType()

Function-aware expression support is needed; this most typically refers to special operators related to datatypes such as JSON or ARRAY

Result value processing is needed, which may include types such as DateTime, Boolean, Enum, or again special datatypes such as JSON, ARRAY.