import sqlite3
DB_NAME = "DATA/intelligence_platform.db"
#Connecting the database to python
def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
