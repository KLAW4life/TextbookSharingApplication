import sqlite3
from contextlib import contextmanager
from config import DATABASE_PATH

# Context manager to handle database connections
@contextmanager
def get_db_connection():
    """Yield a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def create_tables(conn):
    """Create all necessary database tables using the provided connection."""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS textbooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                price REAL,
                condition TEXT,
                description TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password BLOB NOT NULL,
                email TEXT UNIQUE
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_listings (
                listing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                textbook_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (textbook_id) REFERENCES textbooks (id)
            );
        """)
        conn.commit()
        print("All tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def add_user(conn, username, hashed_password, email):
    """Add a new user to the users table with a pre-hashed password."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, hashed_password, email) VALUES (?, ?, ?)
    """, (username, hashed_password, email))
    conn.commit()
    print("User added successfully.")

def add_user_listing(conn, user_id, textbook_id):
    """Add a listing to the user_listings table."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_listings (user_id, textbook_id) VALUES (?, ?)
    """, (user_id, textbook_id))
    conn.commit()
    print("User listing added successfully.")

def fetch_user_listings(conn, user_id):
    """Fetch listings for a specific user."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM textbooks JOIN user_listings ON textbooks.id = user_listings.textbook_id WHERE user_listings.user_id = ?
    """, (user_id,))
    listings = cursor.fetchall()
    return listings
