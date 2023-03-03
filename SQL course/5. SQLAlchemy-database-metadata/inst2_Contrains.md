## Declaring Simple Constraints
The first Column in the above user_table includes the Column.primary_key parameter which is a shorthand technique of indicating that this Column should be part of the primary key for this table. The primary key itself is normally declared implicitly and is represented by the PrimaryKeyConstraint construct, which we can see on the Table.primary_key attribute on the Table object:

>>> user_table.primary_key
PrimaryKeyConstraint(Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False))

The constraint that is most typically declared explicitly is the ForeignKeyConstraint object that corresponds to a database foreign key constraint. When we declare tables that are related to each other, SQLAlchemy uses the presence of these foreign key constraint declarations not only so that they are emitted within CREATE statements to the database, but also to assist in constructing SQL expressions.

A ForeignKeyConstraint that involves only a single column on the target table is typically declared using a column-level shorthand notation via the ForeignKey object. Below we declare a second table address that will have a foreign key constraint referring to the user table:

>>> from sqlalchemy import ForeignKey
>>> address_table = Table(
...     "address",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("user_id", ForeignKey("user_account.id"), nullable=False),
...     Column("email_address", String, nullable=False),
... )

The table above also features a third kind of constraint, which in SQL is the “NOT NULL” constraint, indicated above using the Column.nullable parameter.

Tip

When using the ForeignKey object within a Column definition, we can omit the datatype for that Column; it is automatically inferred from that of the related column, in the above example the Integer datatype of the user_account.id column.

In the next section we will emit the completed DDL for the user and address table to see the completed result.