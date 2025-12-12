from app.data.schema import create_tables
from app.services.user_service import load_users_from_file
from app.data.db import connect_db
import importcsv

def already_has_data():
    # Check if data already exists so we don’t duplicate every time.
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cyber_incidents")
    incidents = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM datasets_metadata")
    datasets = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM it_tickets")
    tickets = cur.fetchone()[0]
    conn.close()
    return incidents > 0 and datasets > 0 and tickets > 0

def setup_everything():
    print("Setting up database")
    create_tables()

    print("Loading users")
    load_users_from_file()
    if not already_has_data():
        print("Importing CSVs into database...")
        importcsv.import_cyber_incidents()
        importcsv.import_datasets()
        importcsv.import_it_tickets()
    else:
        print("Data already exists, skipping duplicate import")
    print("Setup complete!")

if __name__ == "__main__":
    setup_everything()