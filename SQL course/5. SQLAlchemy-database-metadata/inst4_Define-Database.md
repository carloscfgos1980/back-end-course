## Defining Table Metadata with the ORM
This ORM-only section will provide an example declaring the same database structure illustrated in the previous section, using a more ORM-centric configuration paradigm. When using the ORM, the process by which we declare Table metadata is usually combined with the process of declaring mapped classes. The mapped class is any Python class we’d like to create, which will then have attributes on it that will be linked to the columns in a database table. While there are a few varieties of how this is achieved, the most common style is known as declarative, and allows us to declare our user-defined classes and Table metadata at once.

Setting up the Registry
When using the ORM, the MetaData collection remains present, however it itself is contained within an ORM-only object known as the registry. We create a registry by constructing it:

>>> from sqlalchemy.orm import registry
>>> mapper_registry = registry()

The above registry, when constructed, automatically includes a MetaData object that will store a collection of Table objects:

>>> mapper_registry.metadata
MetaData()

Instead of declaring Table objects directly, we will now declare them indirectly through directives applied to our mapped classes. In the most common approach, each mapped class descends from a common base class known as the declarative base. We get a new declarative base from the registry using the registry.generate_base() method:

>>> Base = mapper_registry.generate_base()

Tip

The steps of creating the registry and “declarative base” classes can be combined into one step using the historically familiar declarative_base() function:

from sqlalchemy.orm import declarative_base

Base = declarative_base()