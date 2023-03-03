# Steps

1. Create a database (favorite_movies):
sqlite3 favorite_movies.db

2. Open de file
.open favorite_movies.db

3. Create a table
CREATE TABLE movies (id INTEGER, title TEXT, year INTEGER, rating INTEGER);

4. Insert data to database:
INSERT INTO movies( id, title, year, rating ) VALUES (1, "Memento", 2000, 5 );

5. Show the table with format:
.headers ON
.mode column
SELECT * FROM movies;

6. Insert the rest of the data from movie_list.txt

7. Create a new table in order to add the genres
CREATE TABLE genres (movie_id INTEGER, genre TEXT);

8. Add genres data to the new table from <movie_list.txt>

9. Join tables:

SELECT *
FROM shows
LEFT JOIN Lead_actors
ON shows.id = Lead_actors.show_id;

# Connecting the tables 
1. Now, ALTER the movies table by adding a field for referencing to a genre ID. Since the new column will contain an ID, the datatype will be a number. Name it anyway you like (something like genre_id would do perfectly).
2. Next, UPDATE your movies table by supplying every record with a value in the genre_id column, pointing to a record in the genres table.
3. Finally, use a LEFT JOIN on the movies and genres table, matching the IDs. This should combine the tables, showing all movies records along with their genre information.