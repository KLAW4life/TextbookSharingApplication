import os
import pickle
import streamlit as st
from db.db import get_db_connection, create_tables  # Note the updated import for 'create_tables'
from utils.user_functions import *
from db.listing_management import *
from utils.fetch_covers import fetch_book_cover
from st_pages import hide_pages

def load_session_state():
  if os.path.exists('session_state.pkl'):
      try:
          with open('session_state.pkl', 'rb') as f:
              loaded_state = pickle.load(f)
              os.remove('session_state.pkl')
              return loaded_state
      except Exception as e:
          print("Error during loading session state:", e)
  else:
      print("session_state.pkl not found")
      return None

def show_search_results(query=None):
  """Display listings that match the search query."""
  listings = fetch_all_listings()
  if query:
      filtered_listings = [listing for listing in listings if query.lower() in listing[1].lower()]
  else:
      filtered_listings = listings
  if filtered_listings:
      for listing in filtered_listings:
          cover_image_url = fetch_book_cover(listing[3])
          if cover_image_url:
              details_html = f"""
                  <div style="margin-top: 10px; padding: 10px; border-radius: 10px; background-color: #f8f9fa; border: 1px solid #ccc; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                      {'<img src="' + cover_image_url + '" style="float:left; width:150px; margin-right:20px; border-radius:10px;" />' if cover_image_url else ''}
                      <div style="color: #495057; font-size: 20px; font-weight: 500;">{listing[1]}</div>
                      <div style="color: #495057;">
                          <p><strong>Author:</strong> {listing[2]}</p>
                          <p><strong>ISBN:</strong> {listing[3]}</p>
                          <p><strong>Price:</strong> {listing[4]}</p>
                          <p><strong>Condition:</strong> {listing[5]}</p>
                          <p><strong>Description:</strong> {listing[6]}</p>
                      </div>
                  </div>
                  <br style="clear:both;" />   """
              st.markdown(details_html, unsafe_allow_html=True)
          else:
              details_html = f"""
                  <div style="margin-top: 10px; padding: 10px; border-radius: 10px; background-color: #f8f9fa; border: 1px solid #ccc; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                      <div style="color: #495057; font-size: 20px; font-weight: 500;">{listing[1]}</div>
                      <div style="color: #495057;">
                          <p><strong>Author:</strong> {listing[2]}</p>
                          <p><strong>ISBN:</strong> {listing[3]}</p>
                          <p><strong>Price:</strong> {listing[4]}</p>
                          <p><strong>Condition:</strong> {listing[5]}</p>
                          <p><strong>Description:</strong> {listing[6]}</p>
                      </div>
                  </div>
                  <br style="clear:both;" />   """
              st.markdown(details_html, unsafe_allow_html=True)
  else:
      st.error("No matching listings found.")

def show_search_box():
  """Display a search box and handle search submissions."""
  search_query = st.text_input("Search for textbooks", key="search_query")
  search_button = st.button("Search")

  if search_button:
      if search_query:  # Ensure there is a query to search for
          show_search_results(search_query)
      else:
          st.warning("Please enter a search term to proceed.")

def show_add_listing():
  if not st.session_state.get('form_submitted', False):
      with st.form("Add Textbook Form"):
          title = st.text_input("Title", key="book_title")
          author = st.text_input("Author", key="book_author")
          isbn = st.text_input("ISBN", key="book_isbn")
          price = st.text_input("Price", key="book_price")
          condition = st.selectbox("Condition", ["New", "Like New", "Good", "Fair", "Poor"], key="book_condition")
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


def main():
  with get_db_connection() as conn:
      create_tables(conn)  # Make sure all necessary tables are created

  st.title('Textbook Sharing Application')

  # Check if the user is logged in and adjust the available sidebar options accordingly
  if 'username' in st.session_state:
      options = ["Home", "Add Listing", "Manage Listings"]
  else:
      options = ["Home"]

  choice = st.sidebar.selectbox("Choose an option", options, index=0)  # Default to 'Home'

  # Handle user navigation based on their choice
  if choice == "Home":
      st.session_state['current_page'] = 'Home'
  elif choice == "Add Listing":
      st.session_state['current_page'] = 'Add Listing'
  elif choice == "Manage Listings":
      st.session_state['current_page'] = 'Manage Listings'
  # Display content based on the current page
  if st.session_state['current_page'] == 'Home':
      show_search_box()
  elif st.session_state['current_page'] == 'Add Listing':
      show_add_listing()
  elif st.session_state['current_page'] == 'Manage Listings':
      show_manage_listings()

st.set_page_config(
  page_title = "TextbookSharingApplication"
)

loaded_state = load_session_state()
if loaded_state is not None:
  st.session_state["username"] = loaded_state

if __name__ == '__main__':
  main()
  
hide_pages(
    [
        "login",
        "main",
    ]
)

