from sqlalchemy import text
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
BEGIN (implicit)
select 'hello world'
[...] ()
[('hello world',)]
ROLLBACK