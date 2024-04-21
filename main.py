import streamlit as st
from db.db import get_db_connection, create_tables  # Note the updated import for 'create_tables'
from utils.user_functions import show_registration, show_login, show_manage_listings, show_update_listings
from db.listing_management import fetch_all_listings, add_listing
from utils.fetch_covers import fetch_book_cover

def show_search_results(query):
    """Display listings that match the search query."""
    listings = fetch_all_listings()
    if listings:
        filtered_listings = [listing for listing in listings if query.lower() in listing[1].lower()]
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

def main():
    with get_db_connection() as conn:
        create_tables(conn)  # Make sure all necessary tables are created

    st.title('Textbook Sharing Application')

    # Layout for Search and Login
    with st.form("Search Form"):
        search_query = st.text_input("Search for textbooks", key="search_query")
        search_button = st.form_submit_button("Search")
        login_button = st.form_submit_button("Login")

    if search_button and search_query:
        show_search_results(search_query)

    if login_button:
        st.sidebar.write("Login functionality not implemented.")

    if st.button("Add Listing"):
        st.session_state['form_submitted'] = False  # Reset state on button click

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

    # USER LOGIC
    st.sidebar.title("User Operations")
    if 'username' in st.session_state:
        choices = ["Manage Listings", "Update Listings", "Logout"]
    else:
        choices = ["Register", "Login"]

    choice = st.sidebar.selectbox("Choose an option", choices)

    if choice == "Register":
        show_registration()
    elif choice == "Login":
        show_login()
    elif choice == "Manage Listings":
        show_manage_listings()
    elif choice == "Update Listings":
        show_update_listings()
    elif choice == "Logout":
        # Clear session and display logout message
        del st.session_state['username']
        st.success("You have been logged out.")

if __name__ == '__main__':
    main()
