import sqlite3

conn = sqlite3.connect("data/logs.db")
cursor = conn.cursor()

# Get existing columns
cursor.execute("PRAGMA table_info(request_logs)")
columns = [col[1] for col in cursor.fetchall()]

if "provider" not in columns:
    cursor.execute(
        "ALTER TABLE request_logs ADD COLUMN provider TEXT"
    )

if "model_name" not in columns:
    cursor.execute(
        "ALTER TABLE request_logs ADD COLUMN model_name TEXT"
    )

conn.commit()
conn.close()