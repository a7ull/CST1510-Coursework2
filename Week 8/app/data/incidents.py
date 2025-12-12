from app.data.db import connect_db

# read
def get_all_incidents():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents")
    rows = cur.fetchall()
    conn.close()
    return rows

# create
def add_incident(incident_id, timestamp, severity, category, status, description):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cyber_incidents
        (incident_id, timestamp, severity, category, status, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (incident_id, timestamp, severity, category, status, description))
    conn.commit()
    conn.close()

# delete
def delete_incident(incident_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM cyber_incidents
        WHERE incident_id = ?
    """, (incident_id,))
    conn.commit()
    conn.close()
