# Retrieving Data

Let’s retrieve Grandma’s record from the database. To get a single record from the database, use Select.get():

grandma = Person.select().where(Person.name == 'Grandma L.').get()

We can also use the equivalent shorthand Model.get():

grandma = Person.get(Person.name == 'Grandma L.')


Lists of records

Let’s list all the people in the database:

for person in Person.select():
    print(person.name)

# prints:
# Bob
# Grandma L.
# Herb


query = Pet.select().where(Pet.animal_type == 'cat')
for pet in query:
    print(pet.name, pet.owner.name)


There is a big problem with the previous query: because we are accessing pet.owner.name and we did not select this relation in our original query, peewee will have to perform an additional query to retrieve the pet’s owner. This behavior is referred to as N+1 and it should generally be avoided.

For an in-depth guide to working with relationships and joins, refer to the Relationships and Joins documentation.
We can avoid the extra queries by selecting both Pet and Person, and adding a join.

query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))

for pet in query:
    print(pet.name, pet.owner.name)

# prints:
# Kitty Bob
# Mittens Jr Herb


We can do another cool thing here to get bob’s pets. Since we already have an object to represent Bob, we can do this instead:

for pet in Pet.select().where(Pet.owner == uncle_bob):
    print(pet.name)


# Sorting

Let’s make sure these are sorted alphabetically by adding an order_by() clause:

for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
    print(pet.name)

# prints:
# Fido
# Kitty

Let’s list all the people now, youngest to oldest:

for person in Person.select().order_by(Person.birthday.desc()):
    print(person.name, person.birthday)

# prints:
# Bob 1960-01-15
# Herb 1950-05-05
# Grandma L. 1935-03-01


# Combining filter expressions

Peewee supports arbitrarily-nested expressions. Let’s get all the people whose birthday was either:

before 1940 (grandma)
after 1959 (bob)


d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)
query = (Person
         .select()
         .where((Person.birthday < d1940) | (Person.birthday > d1960)))

for person in query:
    print(person.name, person.birthday)

# prints:
# Bob 1960-01-15
# Grandma L. 1935-03-01


Now let’s do the opposite. People whose birthday is between 1940 and 1960:

query = (Person
         .select()
         .where(Person.birthday.between(d1940, d1960)))

for person in query:
    print(person.name, person.birthday)

# prints:
# Herb 1950-05-05


# Aggregates and Prefetch

Now let’s list all the people and how many pets they have:

query = (Person
         .select(Person, Pet)
         .join(Pet, JOIN.LEFT_OUTER)
         .order_by(Person.name, Pet.name))
for person in query:
    # We need to check if they have a pet instance attached, since not all
    # people have pets.
    if hasattr(person, 'pet'):
        print(person.name, person.pet.name)
    else:
        print(person.name, 'no pets')

# prints:
# Bob Fido
# Bob Kitty
# Grandma L. no pets
# Herb Mittens Jr

# prints:
# Bob 2 pets
# Grandma L. 0 pets
# Herb 1 pets


Usually this type of duplication is undesirable. To accommodate the more common (and intuitive) workflow of listing a person and attaching a list of that person’s pets, we can use a special method called prefetch():

query = Person.select().order_by(Person.name).prefetch(Pet)
for person in query:
    print(person.name)
    for pet in person.pets:
        print('  *', pet.name)

# prints:
# Bob
#   * Kitty
#   * Fido
# Grandma L.
# Herb
#   * Mittens Jr


# SQL Functions

One last query. This will use a SQL function to find all people whose names start with either an upper or lower-case G:

expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
for person in Person.select().where(expression):
    print(person.name)

# prints:
# Grandma L.
This is just the basics! You can make your queries as complex as you like. Check the documentation on Querying for more info.

# Database

We’re done with our database, let’s close the connection:

db.close()