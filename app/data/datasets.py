import pandas as pd
from app.data.db import connect_database

def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))

    conn.commit()
    conn.close()

def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    conn.close()
    return df
