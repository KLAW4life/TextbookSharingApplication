import streamlit as st
import requests

st.title('Google Books Searcher')

# Text input for search query
query = st.text_input('Enter a book title, author, or ISBN:', '')

# Button to trigger search
search = st.button('Search')

if search and query:
    api_key = st.secrets["google_books_api_key"]
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        books_data = response.json()

        # Display each book's information
        for book in books_data.get('items', []):
            title = book['volumeInfo'].get('title', 'No title available')
            authors = ', '.join(book['volumeInfo'].get('authors', ['No authors available']))
            description = book['volumeInfo'].get('description', 'No description available')

            st.subheader(title)
            st.write(f"Authors: {authors}")
            st.write(description)
            st.image(book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''), use_column_width=True)
    else:
        st.error('Failed to retrieve data')