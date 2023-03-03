## Cascading Objects into the Session
We now have a User and two Address objects that are associated in a bidirectional structure in memory, but as noted previously in Inserting Rows with the ORM , these objects are said to be in the transient state until they are associated with a Session object.

We make use of the Session that’s still ongoing, and note that when we apply the Session.add() method to the lead User object, the related Address object also gets added to that same Session:

>>> session.add(u1)
>>> u1 in session
True
>>> a1 in session
True
>>> a2 in session
True

The above behavior, where the Session received a User object, and followed along the User.addresses relationship to locate a related Address object, is known as the save-update cascade and is discussed in detail in the ORM reference documentation at Cascades.

The three objects are now in the pending state; this means they are ready to be the subject of an INSERT operation but this has not yet proceeded; all three objects have no primary key assigned yet, and in addition, the a1 and a2 objects have an attribute called user_id which refers to the Column that has a ForeignKeyConstraint referring to the user_account.id column; these are also None as the objects are not yet associated with a real database row:

>>> print(u1.id)
None
>>> print(a1.user_id)
None

It’s at this stage that we can see the very great utility that the unit of work process provides; recall in the section INSERT usually generates the “values” clause automatically, rows were inserted into the user_account and address tables using some elaborate syntaxes in order to automatically associate the address.user_id columns with those of the user_account rows. Additionally, it was necessary that we emit INSERT for user_account rows first, before those of address, since rows in address are dependent on their parent row in user_account for a value in their user_id column.

When using the Session, all this tedium is handled for us and even the most die-hard SQL purist can benefit from automation of INSERT, UPDATE and DELETE statements. When we Session.commit() the transaction all steps invoke in the correct order, and furthermore the newly generated primary key of the user_account row is applied to the address.user_id column appropriately:

>>> session.commit()
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('pkrabs', 'Pearl Krabs')
INSERT INTO address (email_address, user_id) VALUES (?, ?)
[...] ('pearl.krabs@gmail.com', 6)
INSERT INTO address (email_address, user_id) VALUES (?, ?)
[...] ('pearl@aol.com', 6)
COMMIT