import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages

if "authenticated" in st.session_state:
  del st.session_state["authenticated"]
if "username" in st.session_state:
  del st.session_state["username"]
switch_page("login")

hide_pages([
    "login",
])