import sqlite3

db_path = 'data/telecom.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open('schema_output.txt', 'w') as f:
    f.write("--- Schema for customers ---\n")
    cursor.execute("PRAGMA table_info(customers);")
    columns = cursor.fetchall()
    for col in columns:
        f.write(f"Column: {col[1]}, Type: {col[2]}\n")

    f.write("\n--- Sample Data ---\n")
    cursor.execute("SELECT * FROM customers LIMIT 1;")
    rows = cursor.fetchall()
    for row in rows:
        f.write(str(row) + "\n")

conn.close()
