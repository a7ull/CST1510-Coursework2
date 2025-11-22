from app.services.user_service import login_user, register_user,migrate_users_from_file
from app.data.db import connect_database
from app.data.schema import create_all_tables
import pandas as pd
from pathlib import Path

#Database setup
def load_csv_to_table(conn, csv_path, table_name):
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)

    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows into {table_name}")
        return len(df)
    except Exception as e:
        print(f"Skipping duplicates for {table_name}: {e}")
        return 0



def setup_database_complete():
    print("\n=== COMPLETE DATABASE SETUP STARTED ===")

    # 1. Connect
    conn = connect_database()
    print("Connected to database.")

    # 2. Create all tables
    create_all_tables(conn)
    print("Tables created.")

    # 3. Migrate Week 7 users
    migrated = migrate_users_from_file()
    print(f"Migrated {migrated} users from users.txt")

    # 4. Load CSVs
    DATA_DIR = Path("DATA")
    csv_files = {
        "cyber_incidents": DATA_DIR / "cyber_incidents.csv",
        "datasets_metadata": DATA_DIR / "datasets_metadata.csv",
        "it_tickets": DATA_DIR / "it_tickets.csv",
    }

    total_rows = 0
    for table, path in csv_files.items():
        total_rows += load_csv_to_table(conn, path, table)

    print(f"Total CSV rows loaded: {total_rows}")

    # 5. Verification output
    cursor = conn.cursor()
    print("\nTABLE SUMMARY:")
    for table in ["users", "cyber_incidents", "datasets_metadata", "it_tickets"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cursor.fetchone()[0]} rows")

    conn.close()
    print("=== COMPLETE SETUP DONE ===\n")
setup_database_complete()

# ----------------------------------------------------------
# TABLE MENU
# ----------------------------------------------------------
def table_menu():
    print("""
===========================
      TABLE MENU
===========================
1. Incidents
2. Datasets
3. Tickets
4. Exit
===========================
""")
    return input("Select a table: ").strip()


# ----------------------------------------------------------
# CRUD MENU
# ----------------------------------------------------------
def crud_menu(table_name):
    print(f"""
===========================
   {table_name.upper()} MENU
===========================
1. Create
2. View All
3. Update
4. Delete
5. Back to Table Menu
===========================
""")
    return input("Enter choice: ").strip()

# INCIDENT CRUD
from app.data.incidents import (
    insert_incident,
    get_all_incidents,
    update_incident_status,
    delete_incident
)

# DATASETS CRUD
from app.data.datasets import (
    insert_dataset,
    get_all_datasets,
    update_dataset_category,
    delete_dataset
)

# TICKETS CRUD
from app.data.tickets import (
    insert_ticket,
    get_all_tickets,
    update_ticket_status,
    delete_ticket
)


def main():
    print("===== INTELLIGENCE PLATFORM CRUD SYSTEM =====")

    # Init DB only (no automation/migration)
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    while True:
        a = input("Existing user? Yes or No: ")
        if a.lower() in ["yes", "y"]:
            username = input("Username: ")
            password = input("Password: ")

            success, msg = login_user(username, password)
            print(msg)

            if success:
                break  # login passed
            else:
                print("Invalid login. Try again.\n")

        else:
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            register_user(username, password)
            print("Registration complete. You can now log in.\n")

    # Unified two-level menu navigation
    while True:
        table_choice = table_menu()

        if table_choice == "1":   # Incidents
            while True:
                choice = crud_menu("Incidents")
                if choice == "1":
                    timestamp = input("Date: ")
                    intype = input("Incident Type: ")
                    severity = input("Severity: ")
                    status = input("Status: ")
                    desc = input("Description: ")
                    incident_id = insert_incident(timestamp, intype, severity, status, desc, username)
                    print("Incident created with ID:", incident_id)
                elif choice == "2":
                    print(get_all_incidents())
                elif choice == "3":
                    conn = connect_database()
                    id_ = input("Incident ID: ")
                    new_status = input("New Status: ")
                    rows = update_incident_status(conn, id_, new_status)
                    conn.close()
                    print("Rows updated:", rows)
                elif choice == "4":
                    conn = connect_database()
                    id_ = input("Incident ID to delete: ")
                    rows = delete_incident(conn, id_)
                    conn.close()
                    print("Rows deleted:", rows)
                elif choice == "5":
                    break
                else:
                    print("Invalid option.")

        elif table_choice == "2":   # Datasets
            while True:
                choice = crud_menu("Datasets")
                if choice == "1":
                    name = input("Dataset Name: ")
                    rows = input("Number of Rows: ")
                    columns = input("Number of Columns: ")
                    uploaded_by = input("Uploaded_by: ")
                    upload_date = input("Upload_date: ")
                    dataset_id = insert_dataset(name, rows, columns, uploaded_by, upload_date)
                    print("Dataset added with ID:", dataset_id)
                elif choice == "2":
                    print(get_all_datasets())
                elif choice == "3":
                    conn = connect_database()
                    id_ = input("Dataset ID: ")
                    new_name = input("New Name: ")
                    rows = update_dataset_category(conn, id_, new_name)
                    conn.close()
                    print("Rows updated:", rows)
                elif choice == "4":
                    conn = connect_database()
                    id_ = input("Dataset ID to delete: ")
                    rows = delete_dataset(conn, id_)
                    conn.close()
                    print("Rows deleted:", rows)
                elif choice == "5":
                    break
                else:
                    print("Invalid option.")

        elif table_choice == "3":   # Tickets
            while True:
                choice = crud_menu("Tickets")
                if choice == "1":
                    ticket_id = input("Ticket ID: ")
                    priority = input("Priority: ")
                    desc = input("Description: ")
                    status = input("Status: ")
                    assigned = input("Assigned To: ")
                    created = input("Created Date: ")
                    resolved = input("Resolution time in hours: ")
                    new_id = insert_ticket(ticket_id, priority, desc, status,
                                           assigned, created, resolved)
                    print("Ticket created with ID:", new_id)
                elif choice == "2":
                    print(get_all_tickets())
                elif choice == "3":
                    conn = connect_database()
                    id_ = input("Ticket ID: ")
                    new_status = input("New Status: ")
                    rows = update_ticket_status(conn, id_, new_status)
                    conn.close()
                    print("Rows updated:", rows)
                elif choice == "4":
                    conn = connect_database()
                    id_ = input("Ticket ID to delete: ")
                    rows = delete_ticket(conn, id_)
                    conn.close()
                    print("Rows deleted:", rows)
                elif choice == "5":
                    break
                else:
                    print("Invalid option.")

        elif table_choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
main()