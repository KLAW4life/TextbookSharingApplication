import streamlit as st
from db.db import *
import bcrypt

def hash_password(password):
    """Hash a password for storing using bcrypt."""
    # bcrypt.hashpw expects bytes, so encode the password first
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    # bcrypt.checkpw also expects bytes, provided_password must be encoded
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def register_user(username, email, password):
    """Register a user with hashed password."""
    hashed_password = hash_password(password)
    with get_db_connection() as conn:
        add_user(conn, username, hashed_password, email)

def show_registration():
    with st.form("Register"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        if submit:
            if username and email and password:
                register_user(username, email, password)
                st.success("Registered Successfully!")
            else:
                st.error("Please fill out all fields.")

def verify_login(username, provided_password):
    """Verify user login by checking the hashed password."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            stored_password = result[0]  # No need to encode, it's already in bytes
            return verify_password(stored_password, provided_password)
        return False

def show_login():
    with st.form("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if verify_login(username, password):
                st.session_state['username'] = username  # Setting up session
                st.success("Logged in successfully!")
            else:
                st.error("Incorrect username or password.")

def show_manage_listings():
    if 'username' in st.session_state:
        with get_db_connection() as conn:
            user_listings = fetch_user_listings(conn, st.session_state['username'])
            for listing in user_listings:
                st.write(f"Title: {listing['title']}")  # Add more details and edit options
    else:
        st.warning("Please login to manage listings.")

def update_listing(listing_id, new_data):
    """Update a listing."""
    with get_db_connection() as conn:
        # Assuming update logic is correctly implemented in your db.py
        # Example: update_user_listing(conn, listing_id, new_data)
        pass

def show_update_listings():
    if 'username' in st.session_state:
        listing_id = st.text_input("Listing ID")
        new_title = st.text_input("New Title")
        submit = st.button("Update Listing")
        if submit and listing_id and new_title:
            update_listing(listing_id, {'title': new_title})
            st.success("Listing updated successfully!")
    else:
        st.warning("Please login to update listings.")
