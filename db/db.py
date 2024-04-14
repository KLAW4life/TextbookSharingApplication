import sqlite3
from sqlite3 import Error
from config import DATABASE_PATH

def connect_db():
    """Create a database connection to the SQLite database specified by DATABASE_PATH."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        print("Connection to SQLite DB successful")
        return conn
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_table():
    """Create textbooks table if it doesn't already exist."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS textbooks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT UNIQUE NOT NULL,
                    price REAL,
                    condition TEXT,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            print("Table created successfully.")
        except Error as e:
            print(f"Error '{e}' occurred while creating table")
        finally:
            conn.close()
