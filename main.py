from app.data.db import connect_database
from app.data.schema import create_all_tables

from app.services.user_service import (
    register_user,
    login_user,
    migrate_users_from_file
)

from app.data.incidents import insert_incident, get_all_incidents
from app.data.datasets import insert_dataset, get_all_datasets
from app.data.tickets import insert_ticket, get_all_tickets

import pandas as pd
from pathlib import Path


# ----------------------------------------------------------
# PART 9 — COMPLETE AUTOMATED DATABASE SETUP
# ----------------------------------------------------------
def load_csv_to_table(conn, csv_path, table_name):
    """Load a CSV file into the database."""
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into {table_name}")
    return len(df)


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


# ----------------------------------------------------------
# PART 10 — COMPREHENSIVE TESTING
# ----------------------------------------------------------
def run_comprehensive_tests():
    print("\n===== RUNNING COMPREHENSIVE TEST SUITE =====")

    # 1. Test authentication
    ok, msg = register_user("test_user", "TestPass123!", "user")
    print("[REGISTER]", msg)

    ok, msg = login_user("test_user", "TestPass123!")
    print("[LOGIN]", msg)

    # 2. Test Incident CRUD
    conn = connect_database()
    print("\nTesting Incident Creation...")

    incident_id = insert_incident(
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"Incident #{incident_id} created successfully.")
# ----------------------------------------------------------
# MAIN EXECUTION FLOW
# ----------------------------------------------------------
def main():
    print("======================================")
    print("   WEEK 8 — DATABASE DEMO PROGRAM     ")
    print("======================================")

    # Run Part 9 automatically
    setup_database_complete()

    # Run Part 10 automatically
    run_comprehensive_tests()

    # Your normal demo:
    print("\n=== DEMO: Creating a Regular Incident ===")
    incident_id = insert_incident(
        "2024-11-10",
        "Phishing",
        "High",
        "Open",
        "Suspicious link clicked.",
        "alice"
    )
    print("Created incident with ID:", incident_id)

    print("\n=== All Incidents ===")
    print(get_all_incidents())


if __name__ == "__main__":
    main()
