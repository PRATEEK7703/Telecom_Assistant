import sqlite3

db_path = 'data/telecom.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Schema for customers ---")
cursor.execute("PRAGMA table_info(customers);")
columns = cursor.fetchall()
for col in columns:
    print(f"Column: {col[1]}, Type: {col[2]}")

print("\n--- Sample Email Data ---")
# Try to find an email-like column
email_col = next((c[1] for c in columns if 'email' in c[1].lower()), None)
if email_col:
    print(f"Found email column: {email_col}")
    cursor.execute(f"SELECT {email_col} FROM customers LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
else:
    print("No column with 'email' in name found. Printing first 5 rows:")
    cursor.execute("SELECT * FROM customers LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

conn.close()
