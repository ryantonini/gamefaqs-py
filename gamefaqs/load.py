import sqlite3
import os

here = os.path.dirname(__file__)
db_filename = 'gamefaqs.db'

# create sqlite database and load schema
def load_data():
    with sqlite3.connect(db_filename) as con:
        with open(os.path.join(here, 'data', 'db_schema.sql'), 'r') as f:
            sql = f.read()
            con.executescript(sql)
    con.close()

if __name__ == '__main__':
    load_data()
