## ORM-enabled DELETE Statements
Like UPDATE operations, there is also an ORM-enabled version of DELETE which we can illustrate by using the delete() construct with Session.execute(). It also has a feature by which non expired objects (see expired) that match the given deletion criteria will be automatically marked as “deleted” in the Session:

>>> # refresh the target object for demonstration purposes
>>> # only, not needed for the DELETE
>>> squidward = session.get(User, 4)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (4,)

>>> session.execute(delete(User).where(User.name == "squidward"))
DELETE FROM user_account WHERE user_account.name = ?
[...] ('squidward',)
<sqlalchemy.engine.cursor.CursorResult object at 0x...>

The squidward identity, like that of patrick, is now also in a deleted state. Note that we had to re-load squidward above in order to demonstrate this; if the object were expired, the DELETE operation would not take the time to refresh expired objects just to see that they had been deleted:

>>> squidward in session
False