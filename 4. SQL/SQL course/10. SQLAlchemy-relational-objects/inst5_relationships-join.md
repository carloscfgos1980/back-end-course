## Using Relationships in Queries
The previous section introduced the behavior of the relationship() construct when working with instances of a mapped class, above, the u1, a1 and a2 instances of the User and Address classes. In this section, we introduce the behavior of relationship() as it applies to class level behavior of a mapped class, where it serves in several ways to help automate the construction of SQL queries.

Using Relationships to Join
The sections Explicit FROM clauses and JOINs and Setting the ON Clause introduced the usage of the Select.join() and Select.join_from() methods to compose SQL JOIN clauses. In order to describe how to join between tables, these methods either infer the ON clause based on the presence of a single unambiguous ForeignKeyConstraint object within the table metadata structure that links the two tables, or otherwise we may provide an explicit SQL Expression construct that indicates a specific ON clause.

When using ORM entities, an additional mechanism is available to help us set up the ON clause of a join, which is to make use of the relationship() objects that we set up in our user mapping, as was demonstrated at Declaring Mapped Classes. The class-bound attribute corresponding to the relationship() may be passed as the single argument to Select.join(), where it serves to indicate both the right side of the join as well as the ON clause at once:

>>> print(select(Address.email_address).select_from(User).join(User.addresses))
SELECT address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id

The presence of an ORM relationship() on a mapping is not used by Select.join() or Select.join_from() if we don’t specify it; it is not used for ON clause inference. This means, if we join from User to Address without an ON clause, it works because of the ForeignKeyConstraint between the two mapped Table objects, not because of the relationship() objects on the User and Address classes:

>>> print(select(Address.email_address).join_from(User, Address))
SELECT address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id