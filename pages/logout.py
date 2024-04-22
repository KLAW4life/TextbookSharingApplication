import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

if "authenticated" in st.session_state:
  del st.session_state["authenticated"]
if "username" in st.session_state:
  del st.session_state["username"]
switch_page("login")
