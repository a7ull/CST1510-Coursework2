import bcrypt
from pathlib import Path

from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user

DATA_DIR = Path("DATA")

def register_user(username, password, role="user"):
    if get_user_by_username(username):
        return False, f"Username '{username}' already exists."

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered."

def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]
    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return True, "Login successful."

    return False, "Incorrect password."

def migrate_users_from_file(filepath=DATA_DIR / "users.txt"):
    conn = connect_database()
    cursor = conn.cursor()

    if not filepath.exists():
        return 0

    migrated = 0
    with open(filepath) as f:
        for line in f:
            if not line.strip():
                continue

            username, password_hash, *role = line.strip().split(",")
            role = role[0] if role else "user"

            cursor.execute("""
                INSERT OR IGNORE INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, password_hash, role))

            if cursor.rowcount > 0:
                migrated += 1

    conn.commit()
    conn.close()
    return migrated
