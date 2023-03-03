from datetime import date
from peewee import *

db = SqliteDatabase('people.db')


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db  # this model uses the "people.db" database


db.connect()


db.create_tables([Person, Pet])

''''''
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
'''I need to coment .saved() otherwise it will create me this row everytime I run python'''
# uncle_bob.save()  # bob is now stored in the database
# Returns: 1
grandma = Person(name='Grandma', birthday=date(1935, 3, 1))
herb = Person(name='Herb', birthday=date(1950, 5, 5))

bob_kitty = Pet(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet(owner=herb, name='Mittens Jr', animal_type='cat')
'''
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

grandma.name = 'Grandma L.'
grandma.save()  # Update grandma's name in the database.

# This method will create new rows every time that I run Python
bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')
'''

'''
herb_mittens.delete_instance()

'''


# update class Pet
herb_fido.owner = uncle_bob
herb_fido.save()


grandma = Person.get(Person.name == 'Grandma L.')
print(grandma)

for person in Person.select():
    print(person.name)

'''
query = Pet.select().where(Pet.animal_type == 'cat')
for pet in query:
    print(pet.name, pet.owner.name)
'''
query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))

for pet in query:
    print(pet.name, pet.owner.name)

'''
# Looping thru class Pet and selecting the kitty that belong to certain person (Bob)
for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
    print(pet.name)
'''

for pet in Pet.select().where(Pet.owner == uncle_bob):
    print(pet.name)


for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
    print(pet.name)

for person in Person.select().order_by(Person.birthday.desc()):
    print(person.name, person.birthday)


d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)
query = (Person
         .select()
         .where((Person.birthday < d1940) | (Person.birthday > d1960)))

for person in query:
    print(person.name, person.birthday)

query = (Person
         .select()
         .where(Person.birthday.between(d1940, d1960)))

for person in query:
    print('people between 1940 and 1960:\n', person.name, person.birthday)


# Aggregates and Prefetch
'''
for person in Person.select():
    print('Amount of pets per person:\n',
          person.name, person.pets.count(), 'pets')
'''

'''
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
'''
query = Person.select().order_by(Person.name).prefetch(Pet)
for person in query:
    print(person.name)
    for pet in person.pets:
        print('  *', pet.name)


expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
for person in Person.select().where(expression):
    print('name with a g:', person.name)
