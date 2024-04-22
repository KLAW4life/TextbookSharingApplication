import streamlit as st
from db.db import get_db_connection, add_user
from db.listing_management import *
import bcrypt


def hash_password(password):
  """Hash a password for storing using bcrypt."""
  return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(stored_password, provided_password):
  """Verify a stored password against one provided by user."""
  return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


def show_manage_listings():
  if 'username' in st.session_state:
    with get_db_connection() as conn:
      user_listings = fetch_user_listings(conn, st.session_state['username'])
      if user_listings:
        for listing in user_listings:
          st.write(f"Title: {listing['title']}"
                   )  # Add more details and edit options
      else:
        st.warning("No listings found for this user.")
  else:
    st.warning("Please login to manage listings."
               )  # Add more details and edit options


def update_listing(listing_id, new_data):
  """Update a listing."""
  with get_db_connection() as conn:
    # Assuming update logic is correctly implemented in your db.py
    # Example: update_user_listing(conn, listing_id, new_data)
    pass


def show_update_listings():
  if not st.session_state.get('username'):
      st.warning("Please login to update listings.")
      return

  listing_id = st.text_input("Listing ID")
  new_title = st.text_input("New Title")
  submit = st.button("Update Listing")
  if submit and listing_id and new_title:
      update_listing(listing_id, {'title': new_title})
      st.success("Listing updated successfully!")

  listing_id = st.text_input("Listing ID")
  new_title = st.text_input("New Title")
  submit = st.button("Update Listing")
  if submit and listing_id and new_title:
    update_listing(listing_id, {'title': new_title})
    st.success("Listing updated successfully!")

# def show_forgot_password():
#   st.subheader("Forgot Password")
#   email = st.text_input("Enter your email address")
#   if st.button("Request Reset Link"):
#       if handle_forgot_password(email):
#           st.success("If this email is registered, a reset link will be sent shortly.")
#           st.session_state['show_forgot_password'] = False  # Reset the view
#       else:
#           st.error("There was an error processing your request.")

#   if st.button("Back to Login"):
#       st.session_state['show_forgot_password'] = False
#       st.experimental_rerun()