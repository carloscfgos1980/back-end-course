## Common Relationship Operators
There are some additional varieties of SQL generation helpers that come with relationship(), including:

many to one equals comparison - a specific object instance can be compared to many-to-one relationship, to select rows where the foreign key of the target entity matches the primary key value of the object given:

>>> print(select(Address).where(Address.user == u1))
SELECT address.id, address.email_address, address.user_id
FROM address
WHERE :param_1 = address.user_id

many to one not equals comparison - the not equals operator may also be used:

>>> print(select(Address).where(Address.user != u1))
SELECT address.id, address.email_address, address.user_id
FROM address
WHERE address.user_id != :user_id_1 OR address.user_id IS NULL

object is contained in a one-to-many collection - this is essentially the one-to-many version of the “equals” comparison, select rows where the primary key equals the value of the foreign key in a related object:

>>> print(select(User).where(User.addresses.contains(a1)))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.id = :param_1

An object has a particular parent from a one-to-many perspective - the with_parent() function produces a comparison that returns rows which are referred towards by a given parent, this is essentially the same as using the == operator with the many-to-one side:

>>> from sqlalchemy.orm import with_parent
>>> print(select(Address).where(with_parent(u1, User.addresses)))
SELECT address.id, address.email_address, address.user_id
FROM address
WHERE :param_1 = address.user_id