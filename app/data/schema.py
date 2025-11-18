def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("Users table created.")

def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            severity TEXT,
            category TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT
        );
    """)
    conn.commit()
    print("Cyber Incidents table created.")

def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS datasets_metadata(
        dataset_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL, 
        rows INTEGER,
        columns INTEGER,
        uploaded_by TEXT,
        upload_date TEXT
    );
    """)
    conn.commit()
    print("Datasets Metadata table created.")

def create_it_tickets_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
    ticket_id INTEGER PRIMARY KEY,
    priority TEXT,                  
    description TEXT,
    status TEXT,                    
    assigned_to TEXT,               
    created_at TEXT NOT NULL,       
    resolution_time_hours INTEGER   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    print("IT Tickets table created.")

def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
