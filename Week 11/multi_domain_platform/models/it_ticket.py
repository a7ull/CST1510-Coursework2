from multi_domain_platform.database.db import connect_db

class ITTicket:
    def __init__(self, ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
        self.ticket_id = ticket_id
        self.priority = priority
        self.description = description
        self.status = status
        self.assigned_to = assigned_to
        self.created_at = created_at
        self.resolution_time_hours = resolution_time_hours

    def save(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO it_tickets
            (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.ticket_id, self.priority, self.description, self.status, self.assigned_to, self.created_at, self.resolution_time_hours))
        conn.commit()
        conn.close()

    def delete(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (self.ticket_id,))
        conn.commit()
        conn.close()

def get_all_tickets():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]