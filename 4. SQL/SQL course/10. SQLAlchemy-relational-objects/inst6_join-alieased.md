## Joining between Aliased targets
In the section ORM Entity Aliases we introduced the aliased() construct, which is used to apply a SQL alias to an ORM entity. When using a relationship() to help construct SQL JOIN, the use case where the target of the join is to be an aliased() is suited by making use of the PropComparator.of_type() modifier. To demonstrate we will construct the same join illustrated at ORM Entity Aliases using the relationship() attributes to join instead:

>>> print(
...     select(User)
...     .join(User.addresses.of_type(address_alias_1))
...     .where(address_alias_1.email_address == "patrick@aol.com")
...     .join(User.addresses.of_type(address_alias_2))
...     .where(address_alias_2.email_address == "patrick@gmail.com")
... )
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN address AS address_1 ON user_account.id = address_1.user_id
JOIN address AS address_2 ON user_account.id = address_2.user_id
WHERE address_1.email_address = :email_address_1
AND address_2.email_address = :email_address_2

To make use of a relationship() to construct a join from an aliased entity, the attribute is available from the aliased() construct directly:

>>> user_alias_1 = aliased(User)
>>> print(select(user_alias_1.name).join(user_alias_1.addresses))
SELECT user_account_1.name
FROM user_account AS user_account_1
JOIN address ON user_account_1.id = address.user_id