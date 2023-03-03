## 

The ON Clause is inferred

When using Select.join_from() or Select.join(), we may observe that the ON clause of the join is also inferred for us in simple foreign key cases. More on that in the next section.

We also have the option to add elements to the FROM clause explicitly, if it is not inferred the way we want from the columns clause. We use the Select.select_from() method to achieve this, as below where we establish user_table as the first element in the FROM clause and Select.join() to establish address_table as the second:

>>> print(select(address_table.c.email_address).select_from(user_table).join(address_table))
SELECT address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id

Another example where we might want to use Select.select_from() is if our columns clause doesn’t have enough information to provide for a FROM clause. For example, to SELECT from the common SQL expression count(*), we use a SQLAlchemy element known as sqlalchemy.sql.expression.func to produce the SQL count() function:

>>> from sqlalchemy import func
>>> print(select(func.count("*")).select_from(user_table))
SELECT count(:count_2) AS count_1
FROM user_account

## Setting the ON Clause
The previous examples of JOIN illustrated that the Select construct can join between two tables and produce the ON clause automatically. This occurs in those examples because the user_table and address_table Table objects include a single ForeignKeyConstraint definition which is used to form this ON clause.

If the left and right targets of the join do not have such a constraint, or there are multiple constraints in place, we need to specify the ON clause directly. Both Select.join() and Select.join_from() accept an additional argument for the ON clause, which is stated using the same SQL Expression mechanics as we saw about in The WHERE clause:

>>> print(
...     select(address_table.c.email_address)
...     .select_from(user_table)
...     .join(address_table, user_table.c.id == address_table.c.user_id)
... )
SELECT address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id

ORM Tip - there’s another way to generate the ON clause when using ORM entities that make use of the relationship() construct, like the mapping set up in the previous section at Declaring Mapped Classes. This is a whole subject onto itself, which is introduced at length at Using Relationships to Join.

## OUTER and FULL join
Both the Select.join() and Select.join_from() methods accept keyword arguments Select.join.isouter and Select.join.full which will render LEFT OUTER JOIN and FULL OUTER JOIN, respectively:

>>> print(select(user_table).join(address_table, isouter=True))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account LEFT OUTER JOIN address ON user_account.id = address.user_id
>>> print(select(user_table).join(address_table, full=True))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account FULL OUTER JOIN address ON user_account.id = address.user_id