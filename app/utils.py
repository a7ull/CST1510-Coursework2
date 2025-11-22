
from app.data.db import connect_database

def get_db_conn():
    """
    Cached DB connection resource so Streamlit won't re-open connection on every rerun.
    """
    conn = connect_database()  # no db_path passed
    return conn
