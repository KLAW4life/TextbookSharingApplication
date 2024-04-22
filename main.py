import streamlit as st
from db.db import *  # Note the updated import for 'create_tables'
from utils.user_functions import *
from db.listing_management import *
from utils.fetch_covers import fetch_book_cover
from db.password_reset import *
from utils.user_messages import show_inbox, show_send_message

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
    if 'username' in st.session_state:
        options = ["Home", "Add Listing", "Manage Listings", "Messages", "Logout"]
        default_index = options.index('Home') if 'current_page' not in st.session_state else options.index(st.session_state['current_page'])
    else:
        options = ["Home", "Login", "Register", "Forgot Password"]
        default_index = 0

    choice = st.sidebar.selectbox("Choose an option", options, index=default_index)

    if choice == "Home":
        show_search_box()
    elif choice == "Add Listing":
        show_add_listing()
    elif choice == "Manage Listings":
        show_manage_listings()
    elif choice == "Messages" and 'username' in st.session_state:
        show_send_message(st.session_state['username'])
        show_inbox(st.session_state['username'])
    elif choice == "Logout":
        del st.session_state['username']
        st.success("Logged out successfully.")
    elif choice in ["Login", "Register", "Forgot Password"]:
        st.session_state['current_page'] = choice
        globals()[f"show_{choice.lower().replace(' ', '_')}"]()

if __name__ == '__main__':
    main()
