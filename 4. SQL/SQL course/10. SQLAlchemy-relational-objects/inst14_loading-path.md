## Augmenting Loader Strategy Paths
In Augmenting the ON Criteria we illustrated how to add arbitrary criteria to a JOIN rendered with relationship() to also include additional criteria in the ON clause. The PropComparator.and_() method is in fact generally available for most loader options. For example, if we wanted to re-load the names of users and their email addresses, but omitting the email addresses with the sqlalchemy.org domain, we can apply PropComparator.and_() to the argument passed to selectinload() to limit this criteria:

>>> from sqlalchemy.orm import selectinload
>>> stmt = (
...     select(User)
...     .options(
...         selectinload(
...             User.addresses.and_(~Address.email_address.endswith("sqlalchemy.org"))
...         )
...     )
...     .order_by(User.id)
...     .execution_options(populate_existing=True)
... )
>>> for row in session.execute(stmt):
...     print(
...         f"{row.User.name}  ({', '.join(a.email_address for a in row.User.addresses)})"
...     )
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.id
[...] ()
SELECT address.user_id AS address_user_id, address.id AS address_id,
address.email_address AS address_email_address
FROM address
WHERE address.user_id IN (?, ?, ?, ?, ?, ?)
AND (address.email_address NOT LIKE '%' || ?)
[...] (1, 2, 3, 4, 5, 6, 'sqlalchemy.org')
spongebob  ()
sandy  (sandy@squirrelpower.org)
patrick  ()
squidward  ()
ehkrabs  ()
pkrabs  (pearl.krabs@gmail.com, pearl@aol.com)

A very important thing to note above is that a special option is added with .execution_options(populate_existing=True). This option which takes effect when rows are being fetched indicates that the loader option we are using should replace the existing contents of collections on the objects, if they are already loaded. As we are working with a single Session repeatedly, the objects we see being loaded above are the same Python instances as those that were first persisted at the start of the ORM section of this tutorial.