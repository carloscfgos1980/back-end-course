## Updating ORM Objects
In the preceding section Updating and Deleting Rows with Core, we introduced the Update construct that represents a SQL UPDATE statement. When using the ORM, there are two ways in which this construct is used. The primary way is that it is emitted automatically as part of the unit of work process used by the Session, where an UPDATE statement is emitted on a per-primary key basis corresponding to individual objects that have changes on them. A second form of UPDATE is called an “ORM enabled UPDATE” and allows us to use the Update construct with the Session explicitly; this is described in the next section.

Supposing we loaded the User object for the username sandy into a transaction (also showing off the Select.filter_by() method as well as the Result.scalar_one() method):

>>> sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('sandy',)

The Python object sandy as mentioned before acts as a proxy for the row in the database, more specifically the database row in terms of the current transaction, that has the primary key identity of 2:

>>> sandy
User(id=2, name='sandy', fullname='Sandy Cheeks')

If we alter the attributes of this object, the Session tracks this change:

>>> sandy.fullname = "Sandy Squirrel"

The object appears in a collection called Session.dirty, indicating the object is “dirty”:

>>> sandy in session.dirty
True

When the Session next emits a flush, an UPDATE will be emitted that updates this value in the database. As mentioned previously, a flush occurs automatically before we emit any SELECT, using a behavior known as autoflush. We can query directly for the User.fullname column from this row and we will get our updated value back:

>>> sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
UPDATE user_account SET fullname=? WHERE user_account.id = ?
[...] ('Sandy Squirrel', 2)
SELECT user_account.fullname
FROM user_account
WHERE user_account.id = ?
[...] (2,)
>>> print(sandy_fullname)
Sandy Squirrel

We can see above that we requested that the Session execute a single select() statement. However the SQL emitted shows that an UPDATE were emitted as well, which was the flush process pushing out pending changes. The sandy Python object is now no longer considered dirty:

>>> sandy in session.dirty
False

However note we are still in a transaction and our changes have not been pushed to the database’s permanent storage. Since Sandy’s last name is in fact “Cheeks” not “Squirrel”, we will repair this mistake later when we roll back the transaction. But first we’ll make some more data changes.