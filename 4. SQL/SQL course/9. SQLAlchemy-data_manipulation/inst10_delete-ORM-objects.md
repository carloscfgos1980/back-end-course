## Deleting ORM Objects
To round out the basic persistence operations, an individual ORM object may be marked for deletion by using the Session.delete() method. Let’s load up patrick from the database:

>>> patrick = session.get(User, 3)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (3,)

If we mark patrick for deletion, as is the case with other operations, nothing actually happens yet until a flush proceeds:

>>> session.delete(patrick)

Current ORM behavior is that patrick stays in the Session until the flush proceeds, which as mentioned before occurs if we emit a query:

>>> session.execute(select(User).where(User.name == "patrick")).first()
SELECT address.id AS address_id, address.email_address AS address_email_address,
address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id
[...] (3,)
DELETE FROM user_account WHERE user_account.id = ?
[...] (3,)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('patrick',)

Above, the SELECT we asked to emit was preceded by a DELETE, which indicated the pending deletion for patrick proceeded. There was also a SELECT against the address table, which was prompted by the ORM looking for rows in this table which may be related to the target row; this behavior is part of a behavior known as cascade, and can be tailored to work more efficiently by allowing the database to handle related rows in address automatically; the section delete has all the detail on this.

Beyond that, the patrick object instance now being deleted is no longer considered to be persistent within the Session, as is shown by the containment check:

>>> patrick in session
False

However just like the UPDATEs we made to the sandy object, every change we’ve made here is local to an ongoing transaction, which won’t become permanent if we don’t commit it. As rolling the transaction back is actually more interesting at the moment, we will do that in the next section.