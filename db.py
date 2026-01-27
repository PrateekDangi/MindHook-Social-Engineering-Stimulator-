import sqlite3

# Initialize DB and create table if not exists
conn = sqlite3.connect("logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    user_id TEXT,
    event TEXT,
    timestamp TEXT,
    email TEXT,
    password TEXT,
    phone TEXT,
    message TEXT
)
""")
conn.commit()

# Unified logging function
def log_event(user_id, event, timestamp, email=None, password=None, phone=None, message=None):
    cursor.execute("""
        INSERT INTO logs (user_id, event, timestamp, email, password, phone, message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, event, timestamp, email, password, phone, message))
    conn.commit()
