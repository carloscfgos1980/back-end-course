## Loading Relationships
In the last step, we called Session.commit() which emitted a COMMIT for the transaction, and then per Session.commit.expire_on_commit expired all objects so that they refresh for the next transaction.

When we next access an attribute on these objects, we’ll see the SELECT emitted for the primary attributes of the row, such as when we view the newly generated primary key for the u1 object:

>>> u1.id
BEGIN (implicit)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (6,)
6

The u1 User object now has a persistent collection User.addresses that we may also access. As this collection consists of an additional set of rows from the address table, when we access this collection as well we again see a lazy load emitted in order to retrieve the objects:

>>> u1.addresses
SELECT address.id AS address_id, address.email_address AS address_email_address,
address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id
[...] (6,)
[Address(id=4, email_address='pearl.krabs@gmail.com'), Address(id=5, email_address='pearl@aol.com')]

Collections and related attributes in the SQLAlchemy ORM are persistent in memory; once the collection or attribute is populated, SQL is no longer emitted until that collection or attribute is expired. We may access u1.addresses again as well as add or remove items and this will not incur any new SQL calls:

>>> u1.addresses
[Address(id=4, email_address='pearl.krabs@gmail.com'), Address(id=5, email_address='pearl@aol.com')]

While the loading emitted by lazy loading can quickly become expensive if we don’t take explicit steps to optimize it, the network of lazy loading at least is fairly well optimized to not perform redundant work; as the u1.addresses collection was refreshed, per the identity map these are in fact the same Address instances as the a1 and a2 objects we’ve been dealing with already, so we’re done loading all attributes in this particular object graph:

>>> a1
Address(id=4, email_address='pearl.krabs@gmail.com')
>>> a2
Address(id=5, email_address='pearl@aol.com')

The issue of how relationships load, or not, is an entire subject onto itself. Some additional introduction to these concepts is later in this section at Loader Strategies.