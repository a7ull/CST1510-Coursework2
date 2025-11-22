import sqlite3
from pathlib import Path

DB_PATH = Path("DATA/intelligence_platform.db")

def connect_database():
    """Connect to SQLite database."""
    return sqlite3.connect(str(DB_PATH))
