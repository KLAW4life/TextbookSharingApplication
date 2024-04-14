import streamlit as st
import requests

def search_books():
    st.header("Search Bar")

    query = st.text_input('Enter a textbook title, author, or ISBN:', '')
    search = st.button('Search')

    if search and query:
        api_key = st.secrets["google_books_api_key"]
        url = f'https://www.googleapis.com/books/v1/volumes?q={query}+intitle:textbook&key={api_key}'

        response = requests.get(url)

        if response.status_code == 200:
            books_data = response.json()

            if not books_data.get('items'):
                st.write("No results found. Please try a different search term.")
            else:
                for book in books_data.get('items', []):
                    title = book['volumeInfo'].get('title', 'No title available')
                    authors = ', '.join(book['volumeInfo'].get('authors', ['No authors available']))
                    description = book['volumeInfo'].get('description', 'No description available')
                    publisher = book['volumeInfo'].get('publisher', 'Publisher not available')
                    publishedDate = book['volumeInfo'].get('publishedDate', 'Date not available')

                    st.subheader(title)
                    st.write(f"Authors: {authors}")
                    st.write(description)
                    st.write(f"Publisher: {publisher}")
                    st.write(f"Published Date: {publishedDate}")

                    if 'previewLink' in book['volumeInfo']:
                        st.markdown(f"[More Info]({book['volumeInfo']['previewLink']})", unsafe_allow_html=True)
                        st.image(book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''), use_column_width=True)
        else:
            st.error('Failed to retrieve data')
