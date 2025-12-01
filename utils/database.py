import sqlite3
import pandas as pd
from config.config import DB_PATH

def get_database_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def run_query(query, params=None):
    """Executes a SQL query and returns the results as a DataFrame."""
    conn = get_database_connection()
    if conn:
        try:
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.close()
            return None
    return None

def get_table_schema(table_name):
    """Returns the schema of a specific table."""
    query = f"PRAGMA table_info({table_name});"
    return run_query(query)

def get_all_tables():
    """Returns a list of all tables in the database."""
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    return run_query(query)
