## Exercise: Interacting with the database

We have arrived at the final part about SQL. Now that you know all the basic SQL queries, let's try and apply that newfound knowledge by expanding our movies database with genre information.

# Adding more data 
1. Start by opening the previously created favorite_movies.db database in the SQLite interface. 
2. Display the entries in the movies table using a SELECT statement.
3. Use the WHERE statement, in combination with SELECT, to display all movies with a rating of exactly 5.
4. Add 5 more movies in your database using INSERT.
5. Use the SELECT statement again to see if the new movies have indeed been added.

# Making a new table 
Now, let's try and add movie genres to our database. You might think of just supplying our movies table with another string field for the movie genre. However, that would mean we'd have to type the (exact same) name for a genre every time, giving room for error.

Why? Imagine someone adds a record with genre "rom-com", someone else (or yourself) might add another entry with a genre called "romcom". This could be a problem later, when we want to retrieve meaningful data from our database. Editing or adding info for genres dynamically also becomes increasingly difficult when using this method.

The best option is to make a new, seperate table for genres, and then give it an ID which we can use in other tables to point to the corresponding record containing all the relevant genre information. Making this genres table our easily expandable, single source of truth for all genre information.

1. Start by creating the new genres table using a CREATE TABLE statement. Define a column for the ID (this will serve as our primary key), and one for the name of the genre.
2. Add some (5+) genres to the new table using the INSERT statement. Make sure every record has an ID and a name.
3. Display the records in the genres table using SELECT and check if everything is in order.