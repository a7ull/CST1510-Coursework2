from multi_domain_platform.database.db import connect_db

def table_counts():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cyber_incidents")
    cyber = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM datasets_metadata")
    datasets = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM it_tickets")
    tickets = cur.fetchone()[0]
    conn.close()
    return {"cyber_incidents": cyber, "datasets_metadata": datasets, "it_tickets": tickets}