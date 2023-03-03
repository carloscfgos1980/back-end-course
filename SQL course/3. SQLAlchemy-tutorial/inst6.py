from sqlalchemy.orm import Session


'''The Session has a few different creational patterns, but here we will illustrate the most basic one that tracks exactly with how the Connection is used which is to construct it within a context manager:'''
stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table WHERE y > ? ORDER BY x, y
[...] (6,)
x: 6  y: 8
x: 9  y: 10
x: 11  y: 12
x: 13  y: 14
ROLLBACK

'''Also, like the Connection, the Session features “commit as you go” behavior using the Session.commit() method, illustrated below using a textual UPDATE statement to alter some of our data:'''
with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()
BEGIN (implicit)
UPDATE some_table SET y=? WHERE x=?
[...] ((11, 9), (15, 13))
COMMIT