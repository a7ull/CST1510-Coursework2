from app.data.db import connect_db
conn = connect_db()
cur = conn.cursor()
tables = ["cyber_incidents", "datasets_metadata", "it_tickets"]
for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}:", cur.fetchone()[0])
conn.close()