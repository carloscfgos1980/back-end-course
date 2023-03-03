## Loader Strategies
In the section Loading Relationships we introduced the concept that when we work with instances of mapped objects, accessing the attributes that are mapped using relationship() in the default case will emit a lazy load when the collection is not populated in order to load the objects that should be present in this collection.

Lazy loading is one of the most famous ORM patterns, and is also the one that is most controversial. When several dozen ORM objects in memory each refer to a handful of unloaded attributes, routine manipulation of these objects can spin off many additional queries that can add up (otherwise known as the N plus one problem), and to make matters worse they are emitted implicitly. These implicit queries may not be noticed, may cause errors when they are attempted after there’s no longer a database transaction available, or when using alternative concurrency patterns such as asyncio, they actually won’t work at all.

At the same time, lazy loading is a vastly popular and useful pattern when it is compatible with the concurrency approach in use and isn’t otherwise causing problems. For these reasons, SQLAlchemy’s ORM places a lot of emphasis on being able to control and optimize this loading behavior.

Above all, the first step in using ORM lazy loading effectively is to test the application, turn on SQL echoing, and watch the SQL that is emitted. If there seem to be lots of redundant SELECT statements that look very much like they could be rolled into one much more efficiently, if there are loads occurring inappropriately for objects that have been detached from their Session, that’s when to look into using loader strategies.

Loader strategies are represented as objects that may be associated with a SELECT statement using the Select.options() method, e.g.:

for user_obj in session.execute(
    select(User).options(selectinload(User.addresses))
).scalars():
    user_obj.addresses  # access addresses collection already loaded

They may be also configured as defaults for a relationship() using the relationship.lazy option, e.g.:

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_account"

    addresses = relationship("Address", back_populates="user", lazy="selectin")

Each loader strategy object adds some kind of information to the statement that will be used later by the Session when it is deciding how various attributes should be loaded and/or behave when they are accessed.

The sections below will introduce a few of the most prominently used loader strategies.