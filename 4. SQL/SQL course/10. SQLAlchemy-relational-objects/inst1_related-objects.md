## Working with Related Objects
In this section, we will cover one more essential ORM concept, which is how the ORM interacts with mapped classes that refer to other objects. In the section Declaring Mapped Classes, the mapped class examples made use of a construct called relationship(). This construct defines a linkage between two different mapped classes, or from a mapped class to itself, the latter of which is called a self-referential relationship.

To describe the basic idea of relationship(), first we’ll review the mapping in short form, omitting the Column mappings and other directives:

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_account"

    # ... Column mappings

    addresses = relationship("Address", back_populates="user")


class Address(Base):
    __tablename__ = "address"

    # ... Column mappings

    user = relationship("User", back_populates="addresses")

Above, the User class now has an attribute User.addresses and the Address class has an attribute Address.user. The relationship() construct will be used to inspect the table relationships between the Table objects that are mapped to the User and Address classes. As the Table object representing the address table has a ForeignKeyConstraint which refers to the user_account table, the relationship() can determine unambiguously that there is a one to many relationship from User.addresses to User; one particular row in the user_account table may be referred towards by many rows in the address table.

All one-to-many relationships naturally correspond to a many to one relationship in the other direction, in this case the one noted by Address.user. The relationship.back_populates parameter, seen above configured on both relationship() objects referring to the other name, establishes that each of these two relationship() constructs should be considered to be complimentary to each other; we will see how this plays out in the next section.