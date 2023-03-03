Getting Objects by Primary Key from the Identity Map
The primary key identity of the objects are significant to the Session, as the objects are now linked to this identity in memory using a feature known as the identity map. The identity map is an in-memory store that links all objects currently loaded in memory to their primary key identity. We can observe this by retrieving one of the above objects using the Session.get() method, which will return an entry from the identity map if locally present, otherwise emitting a SELECT:

>>> some_squidward = session.get(User, 4)
>>> some_squidward
User(id=4, name='squidward', fullname='Squidward Tentacles')

The important thing to note about the identity map is that it maintains a unique instance of a particular Python object per a particular database identity, within the scope of a particular Session object. We may observe that the some_squidward refers to the same object as that of squidward previously:

>>> some_squidward is squidward
True

The identity map is a critical feature that allows complex sets of objects to be manipulated within a transaction without things getting out of sync.