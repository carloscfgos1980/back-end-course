## Rolling Back
The Session has a Session.rollback() method that as expected emits a ROLLBACK on the SQL connection in progress. However, it also has an effect on the objects that are currently associated with the Session, in our previous example the Python object sandy. While we changed the .fullname of the sandy object to read "Sandy Squirrel", we want to roll back this change. Calling Session.rollback() will not only roll back the transaction but also expire all objects currently associated with this Session, which will have the effect that they will refresh themselves when next accessed using a process known as lazy loading:

>>> session.rollback()
ROLLBACK

To view the “expiration” process more closely, we may observe that the Python object sandy has no state left within its Python __dict__, with the exception of a special SQLAlchemy internal state object:

>>> sandy.__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x...>}

This is the “expired” state; accessing the attribute again will autobegin a new transaction and refresh sandy with the current database row:

>>> sandy.fullname
BEGIN (implicit)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (2,)
'Sandy Cheeks'

We may now observe that the full database row was also populated into the __dict__ of the sandy object:

>>> sandy.__dict__  
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x...>,
 'id': 2, 'name': 'sandy', 'fullname': 'Sandy Cheeks'}

For deleted objects, when we earlier noted that patrick was no longer in the session, that object’s identity is also restored:

>>> patrick in session
True

and of course the database data is present again as well:

>>> session.execute(select(User).where(User.name == "patrick")).scalar_one() is patrick
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('patrick',)
True