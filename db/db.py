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
        # Textbooks table
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

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password BLOB NOT NULL,
                email TEXT UNIQUE
            );
        """)

        # User listings table with cascading deletes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_listings (
                listing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                textbook_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (textbook_id) REFERENCES textbooks (id) ON DELETE CASCADE
            );
        """)

        # Messages table with cascading deletes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                message_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'unread',
                FOREIGN KEY (sender_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (receiver_id) REFERENCES users (user_id) ON DELETE CASCADE
            );
        """)

        # Add indexes for foreign keys for performance improvement
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_textbooks_id ON textbooks(id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_listings_user_id ON user_listings(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_listings_textbook_id ON user_listings(textbook_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_receiver_id ON messages(receiver_id);")

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
        SELECT textbooks.*, user_listings.listing_id FROM textbooks
        JOIN user_listings ON textbooks.id = user_listings.textbook_id
        WHERE user_listings.user_id = ?
    """, (user_id,))
    listings = cursor.fetchall()
    return listings


def fetch_all_users():
    """Fetch all users from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM users")
        users = [{'user_id': row[0], 'username': row[1]} for row in cursor.fetchall()]
    return users
