# SQL Table Joins
Due to the nature of relational databases, it is often desired to join the data from two or more tables. SQL affords us a number of strategies to accomplish this. To demonstrate the differences, we will use 2 tables: shows and actors. The shows table lists a number of shows and their ratings and release year. The lead-actors table contains a list of actors, that may or may not be featured in a show; a null value indicates that the actor has never been in a show. The assumption is that a show has only 1 lead actor.

# Syntax
Joining two tables is essentially selecting data from a specific intersection of these two tables, so a join always starts with a select. Then you can specify which tables you want to join and on what value the tables can be matched.

The general syntax is something like:

SELECT * 
FROM <table_1> 
<type-of-join> <table_2>
ON <table-1>.<column-name> = <table-2>.<column-name>

The ON clause specifies which values correspond to the matching values in the tables. In our case that would be show.id from the shows table and lead_actors.show_id from the lead actors table.

# Inner join
The inner join returns an intersection of the two tables, omitting all values that are not matched. We might use an inner join if we are interested in knowing which lead actors have the best-rated shows. We are fine with omitting actors that have no show that they have starred in, and we are fine with omitting shows that have no lead actors. 


SELECT * FROM shows INNER JOIN Lead_actors ON shows.id = Lead_actors.show_id;


# Left join
A left join returns all the rows from the left, enriched with values from the right table. The left table is essentially table-1 and the right table is... you guessed it, table-2. A scenario for a left join would be if we wanted to know about all the shows in our database and to find out which shows do not have a lead actor.
SELECT *
FROM shows
LEFT JOIN Lead_actors
ON shows.id = Lead_actors.show_id;

# Right join
A right join inverts the left join, using table-2 as the main table. A use case might be if we wanted a view in which we can see all actors and their affiliated show (or lack thereof). Though similar to the left join, the key difference is that this query includes all actors, but not necessarily all shows.
SELECT *
FROM shows
RIGHT JOIN Lead_actors
ON shows.id = Lead_actors.show_id

# Full outer join
A full outer join combines all data regardless of whether it is matched or not. Basically: all data from all tables. In practice, a full outer join is not used often, but an example use case would be to find mismatched or orphaned data in your database. You could perform the join, the filter on the mismatched values to determine which data is not adequately matched.
SELECT *
FROM shows
FULL OUTER JOIN lead_actors
ON shows.id = lead_actors.show_id