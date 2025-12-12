from app.data.db import connect_db
def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # cyber incidents
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT,
        timestamp TEXT,
        severity TEXT,
        category TEXT,
        status TEXT,
        description TEXT
    )
    """)

    # datsets
    cur.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id TEXT,
        name TEXT,
        rows INTEGER,
        columns INTEGER,
        uploaded_by TEXT,
        upload_date TEXT
    )
    """)

    # IT tickets
    cur.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT,
        priority TEXT,
        description TEXT,
        status TEXT,
        assigned_to TEXT,
        created_at TEXT,
        resolution_time_hours REAL
    )
    """)
    conn.commit()
    conn.close()