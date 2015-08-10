import sqlite3

db_filename = 'gamefaqs.db'
schema_filename = 'db_schema.sql'

with sqlite3.connect(db_filename) as conn:
    print 'Creating schema...'
    with open(schema_filename, 'rt') as f:
        schema = f.read()
    conn.executescript(schema)
 