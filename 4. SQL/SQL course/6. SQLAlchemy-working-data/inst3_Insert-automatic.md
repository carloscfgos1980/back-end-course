## INSERT usually generates the “values” clause automatically
The example above made use of the Insert.values() method to explicitly create the VALUES clause of the SQL INSERT statement. This method in fact has some variants that allow for special forms such as multiple rows in one statement and insertion of SQL expressions. However the usual way that Insert is used is such that the VALUES clause is generated automatically from the parameters passed to the Connection.execute() method; below we INSERT two more rows to illustrate this:

>>> with engine.connect() as conn:
...     result = conn.execute(
...         insert(user_table),
...         [
...             {"name": "sandy", "fullname": "Sandy Cheeks"},
...             {"name": "patrick", "fullname": "Patrick Star"},
...         ],
...     )
...     conn.commit()
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] (('sandy', 'Sandy Cheeks'), ('patrick', 'Patrick Star'))
COMMIT

The execution above features “executemany” form first illustrated at Sending Multiple Parameters, however unlike when using the text() construct, we didn’t have to spell out any SQL. By passing a dictionary or list of dictionaries to the Connection.execute() method in conjunction with the Insert construct, the Connection ensures that the column names which are passed will be expressed in the VALUES clause of the Insert construct automatically.


## INSERT…RETURNING
The RETURNING clause for supported backends is used automatically in order to retrieve the last inserted primary key value as well as the values for server defaults. However the RETURNING clause may also be specified explicitly using the Insert.returning() method; in this case, the Result object that’s returned when the statement is executed has rows which can be fetched:

>>> insert_stmt = insert(address_table).returning(
...     address_table.c.id, address_table.c.email_address
... )
>>> print(insert_stmt)
INSERT INTO address (id, user_id, email_address)
VALUES (:id, :user_id, :email_address)
RETURNING address.id, address.email_address

It can also be combined with Insert.from_select(), as in the example below that builds upon the example stated in INSERT…FROM SELECT:

>>> select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
>>> insert_stmt = insert(address_table).from_select(
...     ["user_id", "email_address"], select_stmt
... )
>>> print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))
INSERT INTO address (user_id, email_address)
SELECT user_account.id, user_account.name || :name_1 AS anon_1
FROM user_account RETURNING address.id, address.email_address

Tip

The RETURNING feature is also supported by UPDATE and DELETE statements, which will be introduced later in this tutorial. The RETURNING feature is generally [1] only supported for statement executions that use a single set of bound parameters; that is, it wont work with the “executemany” form introduced at Sending Multiple Parameters. Additionally, some dialects such as the Oracle dialect only allow RETURNING to return a single row overall, meaning it won’t work with “INSERT..FROM SELECT” nor will it work with multiple row Update or Delete forms.

[1]
There is internal support for the psycopg2 dialect to INSERT many rows at once and also support RETURNING, which is leveraged by the SQLAlchemy ORM. However this feature has not been generalized to all dialects and is not yet part of SQLAlchemy’s regular API.