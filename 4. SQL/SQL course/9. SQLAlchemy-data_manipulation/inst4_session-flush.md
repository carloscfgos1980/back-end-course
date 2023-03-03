## Flushing
The Session makes use of a pattern known as unit of work. This generally means it accumulates changes one at a time, but does not actually communicate them to the database until needed. This allows it to make better decisions about how SQL DML should be emitted in the transaction based on a given set of pending changes. When it does emit SQL to the database to push out the current set of changes, the process is known as a flush.

We can illustrate the flush process manually by calling the Session.flush() method:

>>> session.flush()
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('squidward', 'Squidward Tentacles')
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('ehkrabs', 'Eugene H. Krabs')

Above we observe the Session was first called upon to emit SQL, so it created a new transaction and emitted the appropriate INSERT statements for the two objects. The transaction now remains open until we call any of the Session.commit(), Session.rollback(), or Session.close() methods of Session.

While Session.flush() may be used to manually push out pending changes to the current transaction, it is usually unnecessary as the Session features a behavior known as autoflush, which we will illustrate later. It also flushes out changes whenever Session.commit() is called.