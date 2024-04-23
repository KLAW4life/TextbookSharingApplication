import streamlit as st
from utils.user_messages import show_inbox, show_send_message

show_send_message(st.session_state['username'])
show_inbox(st.session_state['username'])