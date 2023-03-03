from sqlalchemy import text
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


# "commit as you go"
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()
BEGIN (implicit)
CREATE TABLE some_table (x int, y int)
[...] ()
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] ((1, 1), (2, 4))
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT



# "begin once"
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )
BEGIN (implicit)
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] ((6, 8), (9, 10))
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT