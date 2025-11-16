import sqlite3
conn = sqlite3.connect('db/users.db')
cursor = conn.cursor()
create_script="""create table if not exists users (
    id integer primary key autoincrement,
    username text not null unique,  
    password_hash text not null,
    role text default 'user'        )"""
cursor.execute(create_script)
conn.commit()