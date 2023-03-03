## SQLAlchemy Turns Python Objects Into Database Entries

https://www.youtube.com/watch?v=AKQ3XEDI9Mw

# Steps:
1. Import the modules:
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

2. Declare the database:
Base = declarative_base()

3. Create the tables: 
- Person (line 8 - 26)
- Things (28 - 42)

4. Set the environment for the database to be created:
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

5. Add data to table Person (line 51 -63)

6. Add data to table Thing (65 - 75)
* After added the data. The session.add and session.commit should be comment, otherwise it shoot an error by trying to add the data again while printing the info from the database.

7. Gettting the data by the database (78 -104)

# THE END!