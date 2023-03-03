## Persisting and Loading Relationships
We can start by illustrating what relationship() does to instances of objects. If we make a new User object, we can note that there is a Python list when we access the .addresses element:

>>> u1 = User(name="pkrabs", fullname="Pearl Krabs")
>>> u1.addresses
[]

This object is a SQLAlchemy-specific version of Python list which has the ability to track and respond to changes made to it. The collection also appeared automatically when we accessed the attribute, even though we never assigned it to the object. This is similar to the behavior noted at Inserting Rows with the ORM where it was observed that column-based attributes to which we don’t explicitly assign a value also display as None automatically, rather than raising an AttributeError as would be Python’s usual behavior.

As the u1 object is still transient and the list that we got from u1.addresses has not been mutated (i.e. appended or extended), it’s not actually associated with the object yet, but as we make changes to it, it will become part of the state of the User object.

The collection is specific to the Address class which is the only type of Python object that may be persisted within it. Using the list.append() method we may add an Address object:

>>> a1 = Address(email_address="pearl.krabs@gmail.com")
>>> u1.addresses.append(a1)

At this point, the u1.addresses collection as expected contains the new Address object:

>>> u1.addresses
[Address(id=None, email_address='pearl.krabs@gmail.com')]

As we associated the Address object with the User.addresses collection of the u1 instance, another behavior also occurred, which is that the User.addresses relationship synchronized itself with the Address.user relationship, such that we can navigate not only from the User object to the Address object, we can also navigate from the Address object back to the “parent” User object:

>>> a1.user
User(id=None, name='pkrabs', fullname='Pearl Krabs')

This synchronization occurred as a result of our use of the relationship.back_populates parameter between the two relationship() objects. This parameter names another relationship() for which complementary attribute assignment / list mutation should occur. It will work equally well in the other direction, which is that if we create another Address object and assign to its Address.user attribute, that Address becomes part of the User.addresses collection on that User object:

>>> a2 = Address(email_address="pearl@aol.com", user=u1)
>>> u1.addresses
[Address(id=None, email_address='pearl.krabs@gmail.com'), Address(id=None, email_address='pearl@aol.com')]

We actually made use of the user parameter as a keyword argument in the Address constructor, which is accepted just like any other mapped attribute that was declared on the Address class. It is equivalent to assignment of the Address.user attribute after the fact:

# equivalent effect as a2 = Address(user=u1)
>>> a2.user = u1