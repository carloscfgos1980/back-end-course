## type_coerce() - a Python-only “cast”
Sometimes there is the need to have SQLAlchemy know the datatype of an expression, for all the reasons mentioned above, but to not render the CAST expression itself on the SQL side, where it may interfere with a SQL operation that already works without it. For this fairly common use case there is another function type_coerce() which is closely related to cast(), in that it sets up a Python expression as having a specific SQL database type, but does not render the CAST keyword or datatype on the database side. type_coerce() is particularly important when dealing with the JSON datatype, which typically has an intricate relationship with string-oriented datatypes on different platforms and may not even be an explicit datatype, such as on SQLite and MariaDB. Below, we use type_coerce() to deliver a Python structure as a JSON string into one of MySQL’s JSON functions:

>>> import json
>>> from sqlalchemy import JSON
>>> from sqlalchemy import type_coerce
>>> from sqlalchemy.dialects import mysql
>>> s = select(type_coerce({"some_key": {"foo": "bar"}}, JSON)["some_key"])
>>> print(s.compile(dialect=mysql.dialect()))
SELECT JSON_EXTRACT(%s, %s) AS anon_1

Above, MySQL’s JSON_EXTRACT SQL function was invoked because we used type_coerce() to indicate that our Python dictionary should be treated as JSON. The Python __getitem__ operator, ['some_key'] in this case, became available as a result and allowed a JSON_EXTRACT path expression (not shown, however in this case it would ultimately be '$."some_key"') to be rendered.