import streamlit as st
from db.db import get_db_connection, fetch_all_users
from db.messages import send_message, get_messages_for_user, fetch_sender_username

def show_send_message(user_id):
    """Display form to send a message."""
    st.subheader("Send a Message")
    users = fetch_all_users()
    user_options = [(u['user_id'], u['username']) for u in users]
    receiver_id_tuple = st.selectbox("Select User", options=user_options, format_func=lambda x: x[1])
    receiver_id = receiver_id_tuple[0]  # Extract integer value from tuple
    message_text = st.text_area("Message")
    if st.button("Send"):
        if receiver_id and message_text:  # Check if inputs are valid
            with get_db_connection() as conn:
                send_message(conn, user_id, receiver_id, message_text)  # Pass the correct parameters
            st.success("Message sent!")
        else:
            st.error("Please select a receiver and enter a message.")

def show_inbox(user_id):
    """Display all received messages for the user."""
    st.subheader("Inbox")
    with get_db_connection() as conn:
        messages = get_messages_for_user(conn, user_id)
        st.write("DEBUG: Messages retrieved from the database:", messages)  # Debug statement
        if messages:
            for message in messages:
                sender_id, receiver_id, message_text, timestamp, status = message
                sender_username = fetch_sender_username(conn, sender_id)  # Fetch sender's username
                st.write(f"DEBUG: Sender ID: {sender_id}, Receiver ID: {receiver_id}, Message: {message_text}, Timestamp: {timestamp}, Status: {status}")  # Debug statement
                st.write(f"From {sender_username}: {message_text} at {timestamp}")
                st.markdown("---")
        else:
            st.write("DEBUG: No messages found for the user.")  # Debug statement
            st.write("You have no messages.")

