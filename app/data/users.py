from app.data.db import connect_database

def get_user_by_username(username):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_user(username, password_hash, role="user"):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, password_hash, role))

    conn.commit()
    conn.close()
