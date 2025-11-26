
from app.data.db import connect_database

def get_db_conn():
    conn = connect_database()
    return conn
