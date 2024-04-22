import sqlite3
from contextlib import contextmanager
from config import DATABASE_PATH

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def send_message(conn, sender_id, receiver_id, message_text):
    """Send a message from sender to receiver."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (?, ?, ?)", (sender_id, receiver_id, message_text))
    conn.commit()
    cursor.close()

def get_messages_for_user(conn, user_id):
    """Retrieve all messages for a specific user."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE receiver_id = ?", (user_id,))
    messages = cursor.fetchall()
    cursor.close()  # Don't forget to close the cursor
    return messages

def fetch_sender_username(conn, sender_id):
    """Fetch the username of the sender."""
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE user_id = ?", (sender_id,))
    sender_username = cursor.fetchone()[0]
    cursor.close()
    return sender_username
