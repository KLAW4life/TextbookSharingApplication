import streamlit as st
import bcrypt
from db.password_reset import handle_forgot_password
from db.db import get_db_connection, add_user
from db.listing_management import *


def hash_password(password):
  """Hash a password for storing using bcrypt."""
  return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(stored_password, provided_password):
  """Verify a stored password against one provided by user."""
  return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


def login_success(message: str, username: str) -> None:
  st.success(message)
  st.session_state["authenticated"] = True
  st.session_state["username"] = username


def login_form(
    title: str = "Authentication",
    user_tablename: str = "users",
    username_col: str = "username",
    password_col: str = "password",
    email_col: str = "email",
    create_title: str = "Create new account :baby: ",
    login_title: str = "Login to existing account :prince: ",
    allow_guest: bool = True,
    guest_title: str = "Guest login :ninja: ",
    reset_title: str = "Forgot password? :question: ",
    create_username_label: str = "Create a unique username",
    create_username_placeholder: str = None,
    create_username_help: str = None,
    create_password_label: str = "Create a password",
    create_password_placeholder: str = None,
    create_password_help:
    str = "⚠️ Password will be stored as plain text. Do not reuse from other websites. Password cannot be recovered.",
    create_submit_label: str = "Create account",
    create_success_message: str = "Account created :tada:",
    login_username_label: str = "Enter your unique username",
    login_username_placeholder: str = None,
    login_username_help: str = None,
    login_password_label: str = "Enter your password",
    login_password_placeholder: str = None,
    login_password_help: str = None,
    login_submit_label: str = "Login",
    login_success_message: str = "Login succeeded :tada:",
    login_error_message: str = "Wrong username/password :x: ",
    guest_submit_label: str = "Guest login",
):

  connection = get_db_connection()

  # User Authentication
  if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

  if "username" not in st.session_state:
    st.session_state["username"] = None

  with st.expander(title, expanded=not st.session_state["authenticated"]):
    if allow_guest:
      create_tab, login_tab, reset_tab, guest_tab = st.tabs([
          create_title,
          login_title,
          reset_title,
          guest_title,
      ])
    else:
      create_tab, login_tab = st.tabs([
          create_title,
          login_title,
      ])

    # Create new account
    with create_tab:
      with st.form(key="create"):

        email = st.text_input("Email", None, None)

        username = st.text_input(
            label=create_username_label,
            placeholder=create_username_placeholder,
            help=create_username_help,
            disabled=st.session_state["authenticated"],
        )

        password = st.text_input(
            label=create_password_label,
            placeholder=create_password_placeholder,
            help=create_password_help,
            type="password",
            disabled=st.session_state["authenticated"],
        )

        if st.form_submit_button(
            label=create_submit_label,
            type="primary",
            disabled=st.session_state["authenticated"],
        ):

          try:
            hashed_password = hash_password(password)
            with connection as conn:
              add_user(conn, username, hashed_password, email)
          except Error as e:
            st.error(f"Failed to create account: {e}")
          else:
            login_success(create_success_message, username)

    # Login to existing account
    with login_tab:
      with st.form(key="login"):
        username = st.text_input(
            label=login_username_label,
            placeholder=login_username_placeholder,
            help=login_username_help,
            disabled=st.session_state["authenticated"],
        )

        password = st.text_input(
            label=login_password_label,
            placeholder=login_password_placeholder,
            help=login_password_help,
            type="password",
            disabled=st.session_state["authenticated"],
        )

        if st.form_submit_button(
            label=login_submit_label,
            disabled=st.session_state["authenticated"],
            type="primary",
        ):
          with connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT hashed_password FROM users WHERE username = ?",
                (username, ))
            result = cursor.fetchone()
          if result and verify_password(result[0], password):
            login_success(login_success_message, username)
          else:
            st.error(login_error_message)

    # Forgot password
    with reset_tab:
      email = st.text_input("Enter your email address")
      if st.button("Request Reset Link"):
        if handle_forgot_password(email):
          st.success(
              "If this email is registered, a reset link will be sent shortly."
          )
          st.session_state['show_forgot_password'] = False  # Reset the view
        else:
          st.error("There was an error processing your request.")

    # Guest login
    if allow_guest:
      with guest_tab:
        if st.button(
            label=guest_submit_label,
            type="primary",
            disabled=st.session_state["authenticated"],
        ):
          st.session_state["authenticated"] = True

    return connection


def main() -> None:
  login_form(
      create_username_placeholder=
      "Username will be visible in the global leaderboard.",
      create_password_placeholder=
      "⚠️ Password will be stored as plain text. You won't be able to recover it if you forget.",
      guest_submit_label="Play as a guest ⚠️ Scores won't be saved",
  )


if __name__ == "__main__":
  main()
