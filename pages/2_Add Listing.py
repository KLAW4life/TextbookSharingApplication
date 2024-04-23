import streamlit as st
from utils.fetch_covers import fetch_book_cover
from db.listing_management import *
from st_pages import hide_pages

if not st.session_state.get('form_submitted', False):
  with st.form("Add Textbook Form"):
    title = st.text_input("Title", key="book_title")
    author = st.text_input("Author", key="book_author")
    isbn = st.text_input("ISBN", key="book_isbn")
    price = st.text_input("Price", key="book_price")
    condition = st.selectbox("Condition",
                             ["New", "Like New", "Good", "Fair", "Poor"],
                             key="book_condition")
    description = st.text_area("Description", key="book_description")
    submit_button = st.form_submit_button("Submit Listing")

    if submit_button:
      thumbnail_url = fetch_book_cover(isbn)
      if thumbnail_url:
        st.image(thumbnail_url, caption="Book Cover")
      else:
        st.error("Cover image not available.")
      add_listing(title, author, isbn, price, condition, description)
      st.session_state['form_submitted'] = True
      st.success("Textbook added successfully!")
    st.session_state['form_submitted'] = False

hide_pages([
    "login",
])
