## EXISTS forms: has() / any()
In the section EXISTS subqueries, we introduced the Exists object that provides for the SQL EXISTS keyword in conjunction with a scalar subquery. The relationship() construct provides for some helper methods that may be used to generate some common EXISTS styles of queries in terms of the relationship.

For a one-to-many relationship such as User.addresses, an EXISTS against the address table that correlates back to the user_account table can be produced using PropComparator.any(). This method accepts an optional WHERE criteria to limit the rows matched by the subquery:

>>> stmt = select(User.fullname).where(
...     User.addresses.any(Address.email_address == "pearl.krabs@gmail.com")
... )
>>> session.execute(stmt).all()
SELECT user_account.fullname
FROM user_account
WHERE EXISTS (SELECT 1
FROM address
WHERE user_account.id = address.user_id AND address.email_address = ?)
[...] ('pearl.krabs@gmail.com',)
[('Pearl Krabs',)]

As EXISTS tends to be more efficient for negative lookups, a common query is to locate entities where there are no related entities present. This is succinct using a phrase such as ~User.addresses.any(), to select for User entities that have no related Address rows:

>>> stmt = select(User.fullname).where(~User.addresses.any())
>>> session.execute(stmt).all()
SELECT user_account.fullname
FROM user_account
WHERE NOT (EXISTS (SELECT 1
FROM address
WHERE user_account.id = address.user_id))
[...] ()
[('Patrick McStar',), ('Squidward Tentacles',), ('Eugene H. Krabs',)]

The PropComparator.has() method works in mostly the same way as PropComparator.any(), except that it’s used for many-to-one relationships, such as if we wanted to locate all Address objects which belonged to “pearl”:

>>> stmt = select(Address.email_address).where(Address.user.has(User.name == "pkrabs"))
>>> session.execute(stmt).all()
SELECT address.email_address
FROM address
WHERE EXISTS (SELECT 1
FROM user_account
WHERE user_account.id = address.user_id AND user_account.name = ?)
[...] ('pkrabs',)
[('pearl.krabs@gmail.com',), ('pearl@aol.com',)]