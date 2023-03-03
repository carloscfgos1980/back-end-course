## Parameter Ordered Updates
Another MySQL-only behavior is that the order of parameters in the SET clause of an UPDATE actually impacts the evaluation of each expression. For this use case, the Update.ordered_values() method accepts a sequence of tuples so that this order may be controlled [2]:

>>> update_stmt = update(some_table).ordered_values(
...     (some_table.c.y, 20), (some_table.c.x, some_table.c.y + 10)
... )
>>> print(update_stmt)
UPDATE some_table SET y=:y, x=(some_table.y + :y_1)

[2]
While Python dictionaries are guaranteed to be insert ordered as of Python 3.7, the Update.ordered_values() method still provides an additional measure of clarity of intent when it is essential that the SET clause of a MySQL UPDATE statement proceed in a specific way.