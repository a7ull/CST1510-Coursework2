from multi_domain_platform.database.db import connect_db

class SecurityIncident:
    def __init__(self, incident_id, timestamp, severity, category, status, description):
        self.incident_id = incident_id
        self.timestamp = timestamp
        self.severity = severity
        self.category = category
        self.status = status
        self.description = description

    def save(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cyber_incidents
            (incident_id, timestamp, severity, category, status, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.incident_id, self.timestamp, self.severity, self.category, self.status, self.description))
        conn.commit()
        conn.close()

    def delete(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM cyber_incidents WHERE incident_id = ?", (self.incident_id,))
        conn.commit()
        conn.close()

def get_all_incidents():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]