import pandas as pd
from app.data.db import connect_database

def insert_ticket(ticket_id, priority, status, category, subject, description,
                  created_date, resolved_date, assigned_to):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description,
         created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject,
          description, created_date, resolved_date, assigned_to))

    conn.commit()
    conn.close()

def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    conn.close()
    return df
