import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_javascript import st_javascript
from st_pages import hide_pages
st.set_page_config(
  page_title = "TextbookSharingApplication"
)

hide_pages(
    [
        "login",
    ]
)

#st.write(st_javascript("window.location.href") + "/main")
st.title("Textbook Sharing Application")

st.write("""# My first app
Hello *world!*
""")
