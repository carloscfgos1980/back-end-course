# SQL Expressions 
By combining different SQL functions, operators and values, we can create SQL expressions. These expressions allow us to do more complex operations, such as sorting and filtering.

# SQL WHERE clause
For example, we might want to retrieve the records for all movies that we rated with a score of 3 or higher. To retrieve records that meet a certain condition, we can use the WHERE clause in our SQL statement:

SELECT column1, column2, ..., columnN
FROM table_name
WHERE [condition];

Now, let's try using the WHERE clause to retrieve all movies from our movies table that are rated with a score of 3 or higher. To do so, issue the following command within the SQLite CLI:

SELECT * FROM movies WHERE rating >= 3;

Let's try another query using the WHERE clause. What if we wanted to retrieve all recent movies, made after the year 2010? Can you guess the SQL query?

Here it is:
SELECT * FROM movies WHERE year > 2010;

# Multiple conditions
We can even combine conditions as follows: 
SELECT * FROM movies WHERE rating = 3 AND year > 2010;


# SQL ORDER BY clause
We might also want to order the records we retrieve, for example by sorting by highest rating first, or newest to oldest. Using the ORDER BY clause in SQL we can do just that. The syntax for this is as follows:

SELECT column1, column2, ..., columnN
FROM table_name 
[WHERE condition]
ORDER BY column1, column2, ..., columnN [ASC | DESC];

As you can see, we can combine the ORDER BY clause with the WHERE clause, if we want to. Also note that we are allowed to use one ore more columns to ORDER BY. Finally, the keywords ASC and DESC represent the choice between ascending and descending order, respectively.

Let's apply this on our movies table. We want to order the previous result first by rating, then secondly by year. Enter the following query in your SQLite CLI:

Ex:
SELECT * FROM movies WHERE rating >= 3 AND year > 1990 ORDER BY rating, year DESC;
SELECT * FROM movies WHERE rating >= 3 AND year > 1990 ORDER BY rating DESC;
SELECT * FROM movies WHERE rating >= 3 AND year > 1990 ORDER BY year DESC;


# SQL LIMIT/OFFSET clauses
As our database table grows as we add more and more records to it, we might want to be able to retrieve the records in portions. For example, we might build a website where we display a list of movies, distributed over different pages. Retrieving records in 'batches' like this can be done utilising the SQL LIMIT clause:

SELECT column1, column2, ..., columnN FROM table_name LIMIT [no of rows];

Let's retrieve the first 10 records from our table by issueing the following command:
SELECT * FROM movies LIMIT 3;

* Order movies by year descending and just the first 3:
SELECT * FROM movies WHERE rating >= 3 AND year > 1990 ORDER BY year DESC LIMIT 3;

If we now want to retrieve the next 10 records, we can use the OFFSET clause like this: 
SELECT * FROM movies LIMIT 10 OFFSET 10;

And the third page, containing records 21-30:
SELECT * FROM movies LIMIT 10 OFFSET 20;

<OFFSET> represents the start point
<LIMIT> represents the quantity