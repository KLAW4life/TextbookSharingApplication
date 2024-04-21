import requests
import streamlit as st

def fetch_book_cover(isbn):
    try:
        api_key = st.secrets["google_books"]["api_key"]
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items")
            if items:
                volume_info = items[0].get("volumeInfo", {})
                image_links = volume_info.get("imageLinks", {})
                thumbnail = image_links.get("thumbnail")
                return thumbnail
    except Exception as e:
        print(f"Error fetching cover image: {e}")
    return None

