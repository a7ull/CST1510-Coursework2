from app.data.db import connect_db

# read
def get_all_tickets():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets")
    rows = cur.fetchall()
    conn.close()
    return rows

# create
def add_ticket(ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_id,
        priority,
        description,
        status,
        assigned_to,
        created_at,
        resolution_time_hours
    ))
    conn.commit()
    conn.close()

# delete
def delete_ticket(ticket_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM it_tickets
        WHERE ticket_id = ?
    """, (ticket_id,))
    conn.commit()
    conn.close()