import sqlite3
import os

here = os.path.dirname(__file__)
db_filename = 'gamefaqs.db'

# load data into sqlite database
def load_data():
    with sqlite3.connect(db_filename) as con:
        with open(os.path.join(here, 'data', 'dump.sql'), 'r') as f:
            sql = f.read() 
            con.executescript(sql) 
    con.close()


