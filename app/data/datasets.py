import pandas as pd
from app.data.db import connect_database

# CREATE
def insert_dataset(name, rows, columns , uploaded_by , upload_date):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (name, rows, columns , uploaded_by , upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (name, rows, columns , uploaded_by , upload_date))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id

# READ
def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC",
        conn
    )
    conn.close()
    return df

# UPDATE (example: category)
def update_dataset_category(conn, dataset_id, new_name):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE datasets_metadata SET name=? WHERE dataset_id=?",
        (new_name, dataset_id)
    )
    conn.commit()
    return cursor.rowcount

# DELETE
def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE dataset_id=?", (dataset_id,))
    conn.commit()
    return cursor.rowcount
