## Adding objects to a Session
To illustrate the addition process step by step, we will create a Session without using a context manager (and hence we must make sure we close it later!):

>>> session = Session(engine)

The objects are then added to the Session using the Session.add() method. When this is called, the objects are in a state known as pending and have not been inserted yet:

>>> session.add(squidward)
>>> session.add(krabs)

When we have pending objects, we can see this state by looking at a collection on the Session called Session.new:

>>> session.new
IdentitySet([User(id=None, name='squidward', fullname='Squidward Tentacles'), User(id=None, name='ehkrabs', fullname='Eugene H. Krabs')])

The above view is using a collection called IdentitySet that is essentially a Python set that hashes on object identity in all cases (i.e., using Python built-in id() function, rather than the Python hash() function).