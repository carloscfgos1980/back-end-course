## Selecting Rows with Core or ORM
For both Core and ORM, the select() function generates a Select construct which is used for all SELECT queries. Passed to methods like Connection.execute() in Core and Session.execute() in ORM, a SELECT statement is emitted in the current transaction and the result rows available via the returned Result object.

ORM Readers - the content here applies equally well to both Core and ORM use and basic ORM variant use cases are mentioned here. However there are a lot more ORM-specific features available as well; these are documented at ORM Querying Guide.

The select() SQL Expression Construct
The select() construct builds up a statement in the same way as that of insert(), using a generative approach where each method builds more state onto the object. Like the other SQL constructs, it can be stringified in place:

>>> from sqlalchemy import select
>>> stmt = select(user_table).where(user_table.c.name == "spongebob")
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1

Also in the same manner as all other statement-level SQL constructs, to actually run the statement we pass it to an execution method. Since a SELECT statement returns rows we can always iterate the result object to get Row objects back:

>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(row)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(1, 'spongebob', 'Spongebob Squarepants')
ROLLBACK

When using the ORM, particularly with a select() construct that’s composed against ORM entities, we will want to execute it using the Session.execute() method on the Session; using this approach, we continue to get Row objects from the result, however these rows are now capable of including complete entities, such as instances of the User class, as individual elements within each row:

>>> stmt = select(User).where(User.name == "spongebob")
>>> with Session(engine) as session:
...     for row in session.execute(stmt):
...         print(row)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)
ROLLBACK

select() from a Table vs. ORM class

While the SQL generated in these examples looks the same whether we invoke select(user_table) or select(User), in the more general case they do not necessarily render the same thing, as an ORM-mapped class may be mapped to other kinds of “selectables” besides tables. The select() that’s against an ORM entity also indicates that ORM-mapped instances should be returned in a result, which is not the case when SELECTing from a Table object.

The following sections will discuss the SELECT construct in more detail.