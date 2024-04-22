import os
import sqlite3
import secrets
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from contextlib import contextmanager
from config import DATABASE_PATH

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def email_registered(email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = ?)"
        cursor.execute(query, (email,))
        return cursor.fetchone()[0] == 1

def send_password_reset_email(email, token):
    sg = SendGridAPIClient(os.getenv('API_KEY'))
    from_email = "no-reply@yourdomain.com"
    subject = "Password Reset Request"
    content = f"""
    Hi,

    You requested a password reset. Please click the link below to reset your password:
    https://yourdomain.com/reset-password?token={token}

    If you did not request a password reset, please ignore this email.
    """
    message = Mail(
        from_email=from_email,
        to_emails=email,
        subject=subject,
        plain_text_content=content
    )
    try:
        response = sg.send(message)
        print(f"Email sent with status code {response.status_code}")
        return response.status_code == 202  # SendGrid uses 202 Accepted for successful send operations
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def generate_password_reset_token():
    return secrets.token_urlsafe()

def handle_forgot_password(email):
    if email_registered(email):
        token = generate_password_reset_token()
        if send_password_reset_email(email, token):
            return True
    return False
