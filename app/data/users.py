import hashlib
from app.data.db import connect_db
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def create_user(username, password, role):
    conn = connect_db()
    cur = conn.cursor()
    hashed = hash_password(password)
    cur.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, hashed, role))
    conn.commit()
    conn.close()
def check_login(username, password):
    conn = connect_db()
    cur = conn.cursor()
    hashed = hash_password(password)
    cur.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
    """, (username, hashed))
    user = cur.fetchone()
    conn.close()
    return user