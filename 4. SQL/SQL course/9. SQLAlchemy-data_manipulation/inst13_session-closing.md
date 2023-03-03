## Closing a Session
Within the above sections we used a Session object outside of a Python context manager, that is, we didn’t use the with statement. That’s fine, however if we are doing things this way, it’s best that we explicitly close out the Session when we are done with it:

>>> session.close()
ROLLBACK

Closing the Session, which is what happens when we use it in a context manager as well, accomplishes the following things:

It releases all connection resources to the connection pool, cancelling out (e.g. rolling back) any transactions that were in progress.

This means that when we make use of a session to perform some read-only tasks and then close it, we don’t need to explicitly call upon Session.rollback() to make sure the transaction is rolled back; the connection pool handles this.

It expunges all objects from the Session.

This means that all the Python objects we had loaded for this Session, like sandy, patrick and squidward, are now in a state known as detached. In particular, we will note that objects that were still in an expired state, for example due to the call to Session.commit(), are now non-functional, as they don’t contain the state of a current row and are no longer associated with any database transaction in which to be refreshed:

>>> squidward.name
Traceback (most recent call last):
  ...
sqlalchemy.orm.exc.DetachedInstanceError: Instance <User at 0x...> is not bound to a Session; attribute refresh operation cannot proceed

The detached objects can be re-associated with the same, or a new Session using the Session.add() method, which will re-establish their relationship with their particular database row:

>>> session.add(squidward)
>>> squidward.name
BEGIN (implicit)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name, user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (4,)
'squidward'

Tip

Try to avoid using objects in their detached state, if possible. When the Session is closed, clean up references to all the previously attached objects as well. For cases where detached objects are necessary, typically the immediate display of just-committed objects for a web application where the Session is closed before the view is rendered, set the Session.expire_on_commit flag to False.