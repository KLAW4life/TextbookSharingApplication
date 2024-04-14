import sqlite3
from sqlite3 import Error
from db.db import connect_db

def add_listing(title, author, isbn, price, condition, description):
    """Insert a new listing into the database."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO textbooks (title, author, isbn, price, condition, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, author, isbn, price, condition, description))
            conn.commit()
            print("New listing added successfully.")  # Debug statement
        except Error as e:
            print(f"Failed to add new listing: {e}")  # Debug statement
        finally:
            conn.close()
    else:
        print("Connection to database failed.")  # Debug statement

def fetch_all_listings():
    """Fetch all listings from the database."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM textbooks")
            listings = cursor.fetchall()
            print("Listings fetched successfully.")
            return listings
        except Error as e:
            print(f"Failed to fetch listings: {e}")
        finally:
            conn.close()
