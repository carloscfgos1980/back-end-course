## Explicit Join + Eager load
If we were to load Address rows while joining to the user_account table using a method such as Select.join() to render the JOIN, we could also leverage that JOIN in order to eagerly load the contents of the Address.user attribute on each Address object returned. This is essentially that we are using “joined eager loading” but rendering the JOIN ourselves. This common use case is achieved by using the contains_eager() option. This option is very similar to joinedload(), except that it assumes we have set up the JOIN ourselves, and it instead only indicates that additional columns in the COLUMNS clause should be loaded into related attributes on each returned object, for example:

>>> from sqlalchemy.orm import contains_eager
>>> stmt = (
...     select(Address)
...     .join(Address.user)
...     .where(User.name == "pkrabs")
...     .options(contains_eager(Address.user))
...     .order_by(Address.id)
... )
>>> for row in session.execute(stmt):
...     print(f"{row.Address.email_address} {row.Address.user.name}")
SELECT user_account.id, user_account.name, user_account.fullname,
address.id AS id_1, address.email_address, address.user_id
FROM address JOIN user_account ON user_account.id = address.user_id
WHERE user_account.name = ? ORDER BY address.id
[...] ('pkrabs',)
pearl.krabs@gmail.com pkrabs
pearl@aol.com pkrabs

Above, we both filtered the rows on user_account.name and also loaded rows from user_account into the Address.user attribute of the returned rows. If we had applied joinedload() separately, we would get a SQL query that unnecessarily joins twice:

>>> stmt = (
...     select(Address)
...     .join(Address.user)
...     .where(User.name == "pkrabs")
...     .options(joinedload(Address.user))
...     .order_by(Address.id)
... )
>>> print(stmt)  # SELECT has a JOIN and LEFT OUTER JOIN unnecessarily
SELECT address.id, address.email_address, address.user_id,
user_account_1.id AS id_1, user_account_1.name, user_account_1.fullname
FROM address JOIN user_account ON user_account.id = address.user_id
LEFT OUTER JOIN user_account AS user_account_1 ON user_account_1.id = address.user_id
WHERE user_account.name = :name_1 ORDER BY address.id