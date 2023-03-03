# SQLite FULL OUTER JOIN Emulation

# Examples:
https://blog.quest.com/an-overview-of-sql-join-types-with-examples/

# Tutorial for right and full join tables:
https://www.sqlitetutorial.net/sqlite-full-outer-join/


# Introduction to SQL FULL OUTER JOIN clause

In theory, the result of the FULL OUTER JOIN is a combination of  a LEFT JOIN and a RIGHT JOIN. The result set of the full outer join has NULL values for every column of the table that does not have a matching row in the other table. For the matching rows, the FULL OUTER JOIN produces a single row with values from columns of the rows in both tables.

The following picture illustrates the result of the FULL OUTER JOIN clause:

-- create and insert data into the dogs table
CREATE TABLE dogs (type TEXT, color TEXT);

INSERT INTO dogs(type, color) 
VALUES('Hunting','Black'), ('Guard','Brown');

-- create and insert data into the cats table
CREATE TABLE cats (type TEXT, color TEXT);

INSERT INTO cats(type, color) 
VALUES('Indoor','White'), ('Outdoor','Black');


Unfortunately, SQLite does not support the RIGHT JOIN clause and also the FULL OUTER JOIN clause. However, you can easily emulate the FULL OUTER JOIN by using the LEFT JOIN clause.

# Emulating SQLite full outer join

The following statement emulates the FULL OUTER JOIN clause in SQLite:



SELECT d.type,
         d.color,
         c.type,
         c.color
FROM dogs d
LEFT JOIN cats c USING(color)
UNION ALL
SELECT d.type,
         d.color,
         c.type,
         c.color
FROM cats c
LEFT JOIN dogs d USING(color)
WHERE d.color IS NULL;


# How the query works.

Because SQLilte does not support the RIGHT JOIN clause, we use the LEFT JOIN clause in the second SELECT statement instead and switch the positions of the cats and dogs tables.
The UNION ALL clause retains the duplicate rows from the result sets of both queries.
The WHERE clause in the second SELECT statement removes rows that already included in the result set of the first SELECT statement.
In this tutorial, you have learned how to use the UNION ALL and LEFT JOIN clauses to emulate the SQLite FULL OUTER JOIN clause.