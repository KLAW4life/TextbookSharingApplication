# Textbook Sharing Application

## Overview
This application is designed to facilitate the sharing of textbooks among students. Users can list textbooks they are willing to share and search for textbooks they need. The application is built using Python and leverages the Streamlit framework for a user-friendly web interface.

## Features
- User authentication system.
- Ability to list and search for textbooks.
- Real-time updates to listings.

## Getting Started

### Prerequisites
Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation
1. Clone the repository or download the source code.
2. Navigate to the project directory and install the required dependencies:
`pip install -r requirements.txt`


### Running the Application
To run the application, execute the following command in the terminal:
`streamllit run login.py

This will start the server, and the application will be accessible via a web browser at `http://localhost:8501`.

### Development
For development, you can edit the application files and the changes will be reflected in real-time through Streamlit.

## Project Structure
- `authn.py`: Handles user authentication.
- `book_search.py`: Provides functionality to search for books.
- `config.py`: Configuration settings for the application.
- `login.py`: Manages user login functionality.
- `utils/`: Utility scripts for various tasks in the application.
- `db/`: Contains database-related files.
- `pages/`: Includes additional Streamlit pages for the application.

## Contributing
Feel free to fork the repository and submit pull requests. You can also open issues to discuss potential changes or report bugs.

