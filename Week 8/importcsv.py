import csv
from app.data.db import connect_db


# cyber incidents
def import_cyber_incidents():
    conn = connect_db()
    cursor = conn.cursor()
    inserted = 0
    with open(r"C:\Users\sures\Downloads\cyber_incidents.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print("Cyber CSV columns:", reader.fieldnames)
        for row in reader:
            cursor.execute("""
                INSERT INTO cyber_incidents 
                (incident_id, timestamp, severity, category, status, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row.get("incident_id"),
                row.get("timestamp"),
                row.get("severity"),
                row.get("category"),
                row.get("status"),
                row.get("description")
            ))
            inserted += 1

    conn.commit()
    conn.close()
    print("Cyber imported:", inserted)



# datasets
def import_datasets():
    conn = connect_db()
    cursor = conn.cursor()
    inserted = 0
    with open(r"C:\Users\sures\Downloads\datasets_metadata.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print("Datasets CSV columns:", reader.fieldnames)
        for row in reader:
            cursor.execute("""
                INSERT INTO datasets_metadata
                (dataset_id, name, rows, columns, uploaded_by, upload_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row.get("dataset_id"),
                row.get("name"),
                row.get("rows"),
                row.get("columns"),
                row.get("uploaded_by"),
                row.get("upload_date")
            ))
            inserted += 1

    conn.commit()
    conn.close()
    print("Datasets imported:", inserted)



# IT tickets
def import_it_tickets():
    conn = connect_db()
    cursor = conn.cursor()
    inserted = 0
    with open(r"C:\Users\sures\Downloads\it_tickets.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print("Tickets CSV columns:", reader.fieldnames)
        for row in reader:
            cursor.execute("""
                INSERT INTO it_tickets
                (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row.get("ticket_id"),
                row.get("priority"),
                row.get("description"),
                row.get("status"),
                row.get("assigned_to"),
                row.get("created_at"),
                row.get("resolution_time_hours")
            ))
            inserted += 1

    conn.commit()
    conn.close()
    print("Tickets imported:", inserted)
