import streamlit as st
from db.listing_management import fetch_all_listings, add_listing


def show_search_results(query):
    """Display listings that match the search query."""
    listings = fetch_all_listings()
    filtered_listings = [listing for listing in listings if query.lower() in listing[1].lower()]

    if filtered_listings:
        for listing in filtered_listings:
            with st.container():
                st.markdown("""
                    <style>
                        .card {
                            margin-top: 10px;
                            padding: 10px;
                            border-radius: 10px;
                            background-color: #f8f9fa;
                            border: 1px solid #ccc;
                            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                        }
                        .card-header {
                            color: #495057;
                            font-size: 20px;
                            font-weight: 500;
                        }
                        .card-body {
                            color: #495057;
                        }
                    </style>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="card">
                        <div class="card-header">{listing[1]}</div>
                        <div class="card-body">
                            <p><strong>Author:</strong> {listing[2]}</p>
                            <p><strong>ISBN:</strong> {listing[3]}</p>
                            <p><strong>Price:</strong> {listing[4]}</p>
                            <p><strong>Condition:</strong> {listing[5]}</p>
                            <p><strong>Description:</strong> {listing[6]}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.error("No matching listings found.")



def main():
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
        with st.form("Add Textbook Form"):
            title = st.text_input("Title", key="book_title")
            author = st.text_input("Author", key="book_author")
            isbn = st.text_input("ISBN", key="book_isbn")
            price = st.text_input("Price", key="book_price")
            condition = st.selectbox("Condition", ["New", "Like New", "Good", "Fair", "Poor"], key="book_condition")
            description = st.text_area("Description", key="book_description")
            submit_button = st.form_submit_button("Submit Listing")

            if submit_button:
                add_listing(title, author, isbn, price, condition, description)
                st.success("Textbook added successfully!")


if __name__ == '__main__':
    main()
