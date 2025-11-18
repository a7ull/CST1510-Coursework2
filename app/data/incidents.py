import pandas as pd
from app.data.db import connect_database
def insert_incident(timestamp, category, severity, status, description, reported_by=None):
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO cyber_incidents
                       (timestamp, category, severity, status, description, reported_by)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (timestamp, category, severity, status, description, reported_by))

        conn.commit()
        incident_id = cursor.lastrowid
        conn.close()
        return incident_id

def get_all_incidents():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY incident_id DESC", conn)
    conn.close()
    return df
