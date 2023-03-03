## Learning about database relational (SQL)

# Start app. Run in the terminal
sqlite3

# Exit the app:
.exit

# Create a database (favorite_movies):
sqlite3 favorite_movies.db

# open de file
.open favorite_movies.db

# Create a table
CREATE TABLE movies (title TEXT, year INTEGER, rating INTEGER);


NULL: The value is a null value
INTEGER: The value is a signed integer, meaning a round number that can be negative
REAL: The value is a floating point value, meaning a number allowing fractions (like 3.14159265359)
TEXT: The value is a text string, stored using the database encoding
BLOB: The value is a blob of data, stored exactly as it was input

# Check if the table exist
.tables


