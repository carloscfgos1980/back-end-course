## Selecting ORM Entities from Unions
The preceding examples illustrated how to construct a UNION given two Table objects, to then return database rows. If we wanted to use a UNION or other set operation to select rows that we then receive as ORM objects, there are two approaches that may be used. In both cases, we first construct a select() or CompoundSelect object that represents the SELECT / UNION / etc statement we want to execute; this statement should be composed against the target ORM entities or their underlying mapped Table objects:

>>> stmt1 = select(User).where(User.name == "sandy")
>>> stmt2 = select(User).where(User.name == "spongebob")
>>> u = union_all(stmt1, stmt2)

For a simple SELECT with UNION that is not already nested inside of a subquery, these can often be used in an ORM object fetching context by using the Select.from_statement() method. With this approach, the UNION statement represents the entire query; no additional criteria can be added after Select.from_statement() is used:

>>> orm_stmt = select(User).from_statement(u)
>>> with Session(engine) as session:
...     for obj in session.execute(orm_stmt).scalars():
...         print(obj)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ? UNION ALL SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[generated in ...] ('sandy', 'spongebob')
User(id=2, name='sandy', fullname='Sandy Cheeks')
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
ROLLBACK

To use a UNION or other set-related construct as an entity-related component in in a more flexible manner, the CompoundSelect construct may be organized into a subquery using CompoundSelect.subquery(), which then links to ORM objects using the aliased() function. This works in the same way introduced at ORM Entity Subqueries/CTEs, to first create an ad-hoc “mapping” of our desired entity to the subquery, then selecting from that that new entity as though it were any other mapped class. In the example below, we are able to add additional criteria such as ORDER BY outside of the UNION itself, as we can filter or order by the columns exported by the subquery:

>>> user_alias = aliased(User, u.subquery())
>>> orm_stmt = select(user_alias).order_by(user_alias.id)
>>> with Session(engine) as session:
...     for obj in session.execute(orm_stmt).scalars():
...         print(obj)
BEGIN (implicit)
SELECT anon_1.id, anon_1.name, anon_1.fullname
FROM (SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
FROM user_account
WHERE user_account.name = ? UNION ALL SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
FROM user_account
WHERE user_account.name = ?) AS anon_1 ORDER BY anon_1.id
[generated in ...] ('sandy', 'spongebob')
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
ROLLBACK