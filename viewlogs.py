import sqlite3

conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

# ==== Phishing Logs ====
print("\n📧 Phishing Email Logs\n")
print("User ID | Event | Timestamp | Email | Password")
print("-" * 80)
for row in cursor.execute("SELECT user_id, event, timestamp, email, password FROM phishing_logs"):
    user_id, event, timestamp, email, password = row
    print(f"{user_id} | {event} | {timestamp} | {email or '-'} | {password or '-'}")

# ==== Smishing Logs ====
print("\n📱 Smishing Logs\n")
print("User ID | Event | Timestamp | Phone | Message")
print("-" * 80)
for row in cursor.execute("SELECT event, timestamp, phone, message FROM smishing_logs"):
    user_id, event, timestamp, phone, message = row
    print(f"{event} | {timestamp} | {phone or '-'} | {message or '-'}")

conn.close()
