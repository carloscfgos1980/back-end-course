## Emitting DDL to the Database
We’ve constructed a fairly elaborate object hierarchy to represent two database tables, starting at the root MetaData object, then into two Table objects, each of which hold onto a collection of Column and Constraint objects. This object structure will be at the center of most operations we perform with both Core and ORM going forward.

The first useful thing we can do with this structure will be to emit CREATE TABLE statements, or DDL, to our SQLite database so that we can insert and query data from them. We have already all the tools needed to do so, by invoking the MetaData.create_all() method on our MetaData, sending it the Engine that refers to the target database:

>>> metadata_obj.create_all(engine)
BEGIN (implicit)
PRAGMA main.table_...info("user_account")
...
PRAGMA main.table_...info("address")
...
CREATE TABLE user_account (
    id INTEGER NOT NULL,
    name VARCHAR(30),
    fullname VARCHAR,
    PRIMARY KEY (id)
)
...
CREATE TABLE address (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    email_address VARCHAR NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES user_account (id)
)
...
COMMIT

The DDL create process by default includes some SQLite-specific PRAGMA statements that test for the existence of each table before emitting a CREATE. The full series of steps are also included within a BEGIN/COMMIT pair to accommodate for transactional DDL (SQLite does actually support transactional DDL, however the sqlite3 database driver historically runs DDL in “autocommit” mode).

The create process also takes care of emitting CREATE statements in the correct order; above, the FOREIGN KEY constraint is dependent on the user table existing, so the address table is created second. In more complicated dependency scenarios the FOREIGN KEY constraints may also be applied to tables after the fact using ALTER.

The MetaData object also features a MetaData.drop_all() method that will emit DROP statements in the reverse order as it would emit CREATE in order to drop schema elements.

Migration tools are usually appropriate

Overall, the CREATE / DROP feature of MetaData is useful for test suites, small and/or new applications, and applications that use short-lived databases. For management of an application database schema over the long term however, a schema management tool such as Alembic, which builds upon SQLAlchemy, is likely a better choice, as it can manage and orchestrate the process of incrementally altering a fixed database schema over time as the design of the application changes.