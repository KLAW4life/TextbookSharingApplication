import sqlite3
from sqlite3 import Error
from db.db import get_db_connection  # Ensure correct import based on your project structure

def add_listing(title, author, isbn, price, condition, description):
    """Add a new listing to the database using context manager."""
    print("add_listing called")  # Debug statement
    sql = """
    INSERT INTO textbooks (title, author, isbn, price, condition, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (title, author, isbn, price, condition, description))
            conn.commit()
            print("New listing added successfully.")
        except sqlite3.Error as e:
            print(f"Failed to add new listing: {e}")

def fetch_all_listings():
    """Fetch all listings from the database using context manager."""
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM textbooks")
            listings = cursor.fetchall()
            print("Listings fetched successfully.")
            return listings
        except sqlite3.Error as e:
            print(f"Failed to fetch listings: {e}")

def fetch_user_listings(conn, username):
    """Fetch listings for a specific user by their username."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.* FROM textbooks t
        JOIN user_listings ul ON t.id = ul.textbook_id
        JOIN users u ON ul.user_id = u.user_id
        WHERE u.username = ?
    """, (username,))
    return cursor.fetchall()