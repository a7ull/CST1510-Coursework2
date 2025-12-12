import bcrypt
from app.data.db import connect_db

# Hash password using bcrypt
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

# Create user with bcrypt-hashed password
def create_user(username, password, role):
    conn = connect_db()
    cur = conn.cursor()

    hashed = hash_password(password)  # this is now a BYTE string (bcrypt)

    cur.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, hashed, role))

    conn.commit()
    conn.close()


# Check login using bcrypt check
def check_login(username, password):
    conn = connect_db()
    cur = conn.cursor()

    # Get the stored hash for the user
    cur.execute("""
        SELECT * FROM users
        WHERE username = ?
    """, (username,))

    user = cur.fetchone()
    conn.close()

    if user is None:
        return None

    stored_hash = user["password"]

    # If it's coming as string from DB, convert to bytes
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("utf-8")
    # password column from DB

    # Compare entered password with stored hash
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return user
    else:
        return None