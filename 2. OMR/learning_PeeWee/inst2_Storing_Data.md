# Storing data

Let’s begin by populating the database with some people. We will use the save() and create() methods to add and update people’s records.

from datetime import date
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save() # bob is now stored in the database
# Returns: 1
Note

When you call save(), the number of rows modified is returned.
You can also add a person by calling the create() method, which returns a model instance:

grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

# Update

To update a row, modify the model instance and call save() to persist the changes. Here we will change Grandma’s name and then save the changes in the database:

grandma.name = 'Grandma L.'
grandma.save()  # Update grandma's name in the database.



# Delete a row

After a long full life, Mittens sickens and dies. We need to remove him from the database:

herb_mittens.delete_instance() # he had a great life
# Returns: 1


# update class Pet

Uncle Bob decides that too many animals have been dying at Herb’s house, so he adopts Fido:

herb_fido.owner = uncle_bob
herb_fido.save()


