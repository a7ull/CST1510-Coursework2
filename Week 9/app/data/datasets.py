from app.data.db import connect_db

# read
def get_all_datasets():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata")
    rows = cur.fetchall()
    conn.close()
    return rows

# create
def add_dataset(dataset_id, name, rows, columns, uploaded_by, upload_date):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO datasets_metadata
        (dataset_id, name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_id, name, rows, columns, uploaded_by, upload_date))
    conn.commit()
    conn.close()

# delete
def delete_dataset(dataset_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM datasets_metadata
        WHERE dataset_id = ?
    """, (dataset_id,))
    conn.commit()
    conn.close()