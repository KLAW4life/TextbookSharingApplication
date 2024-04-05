import streamlit as st
import duo_universal
from streamlit.source_util import get_pages
from streamlit_extras.switch_page_button import switch_page
from st_login_form import login_form
from duo_universal.client import Client, DuoException
import streamlit.components.v1 as components
import webbrowser
from flask import Flask, request, redirect, session, render_template

def TFA(username):
  duo_client = Client(
      client_id="DIF2XDE121PIAYO9OXRF",
      client_secret="5rQvC1JlKncpM03DuyvL64NnO4XDPvjDeNuoGbPq",
      host="api-5f0df9c4.duosecurity.com",
      redirect_uri= get_pages("main"),
  )
  try:
    duo_client.health_check()
  except DuoException:
    st.error("Duo health check failed")
  state = duo_client.generate_state()
  #flask.session['state'] = state
  prompt_uri = duo_client.create_auth_url(username, state)
  components.iframe(prompt_uri)


client = login_form()

if st.session_state["authenticated"]:
  if st.session_state["username"]:
    st.success(f"Welcome {st.session_state['username']}")
    TFA(st.session_state["username"])
  else:
    st.success("Welcome guest")

else:
  st.error("Not authenticated")

st.sidebar.success("Select a page")
