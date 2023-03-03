The foundation of any typical database consists of implementing four functions: Create, Read, Update and Delete (aka CRUD).

# SQL implements these functions with the four statements that we're going to learn about now:
INSERT for Creating
SELECT for Reading
UPDATE for Updating
DELETE for Deleting


# SQL INSERT statement
We can add data to our database using the INSERT statement. Let's start by adding our first movie record in our movies table. The syntax for an insert statement is as follows:
INSERT INTO table_name( column1, column2, ..., columnN )
VALUES ( value1, value2, ..., valueN );

Ex:
INSERT INTO movies( title, year, rating ) VALUES ( "Memento", 2000, 5 );
* Note:
Don't forget the ;


# SQL SELECT statement 
Now, to retrieve and display records stored in our table, we use the SQL statement SELECT:
SELECT column1, column2, ..., columnN
FROM table_name;

Ex:
SELECT title, year, rating FROM movies;

Or equivalently, we can use the wildcard operator *, which also selects all columns:
SELECT * FROM movies;


Note

To get a cleaner view of your tables, consider tweaking some settings: enter .headers ON to display headers, and .mode column to display rows in column style. Enter the SELECT * FROM movies; statement again and notice that the view has changed.

# SQL UPDATE statement
If we want to update some information in our database, we can do so using the UPDATE statement:
UPDATE table_name
SET column1 = value1, column2 = value2, ..., columnN = valueN
WHERE [condition];

EX:
UPDATE movies SET rating = 4 WHERE title = 'Memento';


# SQL DELETE statement 
Finally, the DELETE statement allows us to delete records, also allowing us to supply a condition using the WHERE clause: 
DELETE FROM table_name
WHERE [condition];

Ex:
DELETE FROM movies WHERE title = 'Memento';