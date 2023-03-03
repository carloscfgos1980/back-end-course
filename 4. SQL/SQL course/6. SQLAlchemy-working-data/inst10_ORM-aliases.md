## ORM Entity Aliases
The ORM equivalent of the FromClause.alias() method is the ORM aliased() function, which may be applied to an entity such as User and Address. This produces a Alias object internally that’s against the original mapped Table object, while maintaining ORM functionality. The SELECT below selects from the User entity all objects that include two particular email addresses:

>>> from sqlalchemy.orm import aliased
>>> address_alias_1 = aliased(Address)
>>> address_alias_2 = aliased(Address)
>>> print(
...     select(User)
...     .join_from(User, address_alias_1)
...     .where(address_alias_1.email_address == "patrick@aol.com")
...     .join_from(User, address_alias_2)
...     .where(address_alias_2.email_address == "patrick@gmail.com")
... )
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN address AS address_1 ON user_account.id = address_1.user_id
JOIN address AS address_2 ON user_account.id = address_2.user_id
WHERE address_1.email_address = :email_address_1
AND address_2.email_address = :email_address_2

Tip

As mentioned in Setting the ON Clause, the ORM provides for another way to join using the relationship() construct. The above example using aliases is demonstrated using relationship() at Joining between Aliased targets.