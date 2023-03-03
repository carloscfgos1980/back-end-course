from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Person(Base):
    __tablename__ = "people"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn} {self.firstname} {self.lastname} {self.gender} ({self.age}))"


class Thing(Base):
    __tablename__ = "things"

    tid = Column("tid", Integer, primary_key=True)
    description = Column("description", String)
    owner = Column(Integer, ForeignKey("people.ssn"))

    def __init__(self, tid, description, owner):
        self.tid = tid
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f"{self.tid} {self.description} {self.owner}"


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


person = Person(123, "Mike", "Blue", "m", 35)
# session.add(person)


p1 = Person(456, "Anna", "Biden", "f", 30)
p2 = Person(789, "Carlos", "Infante", "m", 43)
p3 = Person(100, "Flaki", "Rica", "f", 34)

'''I need to comment the session add and commit otherwise when I run the program it will give an error coz the table and the data already exist'''
# session.add(p1)
# session.add(p2)
# session.add(p3)
# session.commit()

t1 = Thing(1, "Car", person.ssn)
t2 = Thing(2, "Laptop", p1.ssn)
t3 = Thing(3, "Celphone", person.ssn)
t4 = Thing(4, "Bike", p2.ssn)
t5 = Thing(5, "Earphones", p3.ssn)
# session.add(t1)
# session.add(t2)
# session.add(t3)
# session.add(t4)
# session.add(t5)
# session.commit()


result = session.query(Person).all()
print(result)

outcome = session.query(Person).filter(Person.firstname == 'Flaki')
for x in outcome:
    print(x)

more = session.query(Person).filter(Person.age >= 35)
for x in more:
    print(x)

# I can filter by just adding a combination of letter that will loop into the database and find the match. Example bellow
otherResult = session.query(Person).filter(Person.firstname.like("%rl%"))
for x in otherResult:
    print(x)

Checking = session.query(Person).filter(
    Person.firstname.in_(["carlos", "Flaki"]))
for x in Checking:
    print(x)

# print the objects to belon to the person and the person data with the folled example
xxx = session.query(Thing, Person).filter(
    Thing.owner == Person.ssn).filter(Person.firstname == "Flaki").all()

for r in xxx:
    print(r)
