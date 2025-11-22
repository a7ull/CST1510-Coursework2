import pandas as pd
from app.data.db import connect_database

# CREATE
def insert_ticket(ticket_id, priority, description,status, assigned_to,created_at, resolution_time_hours):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, description,status, assigned_to,created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, description,status, assigned_to,created_at, resolution_time_hours))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

# READ
def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY ticket_id DESC",
        conn
    )
    conn.close()
    return df

# UPDATE (example: status)
def update_ticket_status(conn, ticket_id, new_status):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE it_tickets SET status=? WHERE ticket_id=?",
        (new_status, ticket_id)
    )
    conn.commit()
    return cursor.rowcount

# DELETE
def delete_ticket(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id=?", (ticket_id,))
    conn.commit()
    return cursor.rowcount
