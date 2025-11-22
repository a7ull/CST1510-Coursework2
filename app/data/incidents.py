import pandas as pd
from app.data.db import connect_database

def insert_incident(timestamp, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents
        (timestamp, category, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY incident_id DESC",
        conn
    )
    conn.close()
    return df
def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status=? WHERE incident_id=?", (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE incident_id=?", (incident_id,))
    conn.commit()
    return cursor.rowcount
