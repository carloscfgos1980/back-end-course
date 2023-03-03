## ORM Entity Subqueries/CTEs
In the ORM, the aliased() construct may be used to associate an ORM entity, such as our User or Address class, with any FromClause concept that represents a source of rows. The preceding section ORM Entity Aliases illustrates using aliased() to associate the mapped class with an Alias of its mapped Table. Here we illustrate aliased() doing the same thing against both a Subquery as well as a CTE generated against a Select construct, that ultimately derives from that same mapped Table.

Below is an example of applying aliased() to the Subquery construct, so that ORM entities can be extracted from its rows. The result shows a series of User and Address objects, where the data for each Address object ultimately came from a subquery against the address table rather than that table directly:

>>> subq = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
>>> address_subq = aliased(Address, subq)
>>> stmt = (
...     select(User, address_subq)
...     .join_from(User, address_subq)
...     .order_by(User.id, address_subq.id)
... )
>>> with Session(engine) as session:
...     for user, address in session.execute(stmt):
...         print(f"{user} {address}")
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname,
anon_1.id AS id_1, anon_1.email_address, anon_1.user_id
FROM user_account JOIN
(SELECT address.id AS id, address.email_address AS email_address, address.user_id AS user_id
FROM address
WHERE address.email_address NOT LIKE ?) AS anon_1 ON user_account.id = anon_1.user_id
ORDER BY user_account.id, anon_1.id
[...] ('%@aol.com',)
User(id=1, name='spongebob', fullname='Spongebob Squarepants') Address(id=1, email_address='spongebob@sqlalchemy.org')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=2, email_address='sandy@sqlalchemy.org')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=3, email_address='sandy@squirrelpower.org')
ROLLBACK

Another example follows, which is exactly the same except it makes use of the CTE construct instead:

>>> cte_obj = select(Address).where(~Address.email_address.like("%@aol.com")).cte()
>>> address_cte = aliased(Address, cte_obj)
>>> stmt = (
...     select(User, address_cte)
...     .join_from(User, address_cte)
...     .order_by(User.id, address_cte.id)
... )
>>> with Session(engine) as session:
...     for user, address in session.execute(stmt):
...         print(f"{user} {address}")
BEGIN (implicit)
WITH anon_1 AS
(SELECT address.id AS id, address.email_address AS email_address, address.user_id AS user_id
FROM address
WHERE address.email_address NOT LIKE ?)
SELECT user_account.id, user_account.name, user_account.fullname,
anon_1.id AS id_1, anon_1.email_address, anon_1.user_id
FROM user_account
JOIN anon_1 ON user_account.id = anon_1.user_id
ORDER BY user_account.id, anon_1.id
[...] ('%@aol.com',)
User(id=1, name='spongebob', fullname='Spongebob Squarepants') Address(id=1, email_address='spongebob@sqlalchemy.org')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=2, email_address='sandy@sqlalchemy.org')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=3, email_address='sandy@squirrelpower.org')
ROLLBACK

See also

Selecting Entities from Subqueries - in the ORM Querying Guide