import sqlite3
import os
from datetime import datetime, timedelta
import random

# Path to the database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "telecom.db")

def init_db():
    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create network_events table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS network_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT,
        severity TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Check if table is empty
    cursor.execute("SELECT count(*) FROM network_events")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Populating network_events with sample data...")
        events = [
            ("Maintenance", "Scheduled maintenance for Sector 7", "Sector 7", "Warning", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
            ("Upgrade", "5G upgrade completed in Downtown area", "Downtown", "Info", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")),
            ("Outage", "Temporary outage reported due to storm", "North Hills", "Critical", (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")),
            ("Latency", "High latency detected in West End", "West End", "Warning", (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")),
        ]
        
        cursor.executemany("INSERT INTO network_events (event_type, description, location, severity, timestamp) VALUES (?, ?, ?, ?, ?)", events)
        conn.commit()
        print("Sample data added.")
    else:
        print("network_events table already has data.")

    # Verify usage_data exists (it should, but good to check)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usage_data'")
    if not cursor.fetchone():
        print("usage_data table missing! Creating sample usage_data...")
        cursor.execute("""
        CREATE TABLE usage_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            data_used_gb REAL,
            data_limit_gb REAL,
            voice_minutes_used INTEGER,
            voice_limit_minutes INTEGER,
            sms_used INTEGER,
            sms_limit INTEGER
        )
        """)
        # Add sample for admin and a customer
        cursor.execute("INSERT INTO usage_data (user_email, data_used_gb, data_limit_gb) VALUES (?, ?, ?)", ("admin@example.com", 45.5, 100.0))
        cursor.execute("INSERT INTO usage_data (user_email, data_used_gb, data_limit_gb) VALUES (?, ?, ?)", ("alice@example.com", 12.3, 50.0))
        conn.commit()

    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
