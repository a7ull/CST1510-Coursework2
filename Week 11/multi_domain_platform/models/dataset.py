from multi_domain_platform.database.db import connect_db

class Dataset:
    def __init__(self, dataset_id, name, rows, columns, uploaded_by, upload_date):
        self.dataset_id = dataset_id
        self.name = name
        self.rows = rows
        self.columns = columns
        self.uploaded_by = uploaded_by
        self.upload_date = upload_date

    def save(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO datasets_metadata
            (dataset_id, name, rows, columns, uploaded_by, upload_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.dataset_id, self.name, self.rows, self.columns, self.uploaded_by, self.upload_date))
        conn.commit()
        conn.close()

    def delete(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM datasets_metadata WHERE dataset_id = ?", (self.dataset_id,))
        conn.commit()
        conn.close()

def get_all_datasets():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]