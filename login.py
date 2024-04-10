import webbrowser
import streamlit as st
import st_pages
from streamlit.components.v1 import components, html
from duo_universal.client import Client, DuoException
from streamlit_extras.switch_page_button import switch_page
from streamlit_javascript import st_javascript
from st_login_form import login_form

def nav_to(url):
  nav_script = """
      <meta http-equiv="refresh" content="0; url='%s'">
  """ % (url)
  st.write(nav_script, unsafe_allow_html=True)

def TFA(username):
  duo_client = Client(
      client_id="DIF2XDE121PIAYO9OXRF",
      client_secret="5rQvC1JlKncpM03DuyvL64NnO4XDPvjDeNuoGbPq",
      host="api-5f0df9c4.duosecurity.com",
      redirect_uri= st_javascript("window.location.origin") + "/main"
  )
  try:
    duo_client.health_check()
  except DuoException:
    st.error("Duo health check failed")
  state = duo_client.generate_state()
  prompt_uri = duo_client.create_auth_url(username, state)
  #components.iframe(prompt_uri,700,700)
  #st_javascript("window.location.replace(prompt_uri)")
  #webbrowser.open(prompt_uri)
  #open_page(prompt_uri)
  nav_to(prompt_uri)

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

placeholder = st.empty()

with placeholder.container():
  client = login_form()

if st.session_state["authenticated"]:
  if st.session_state["username"]:
    st.success(f"Welcome {st.session_state['username']}")
    TFA(st.session_state["username"])
    placeholder.empty()
  else:
    st.success("Welcome guest")

else:
  st.error("Not authenticated")
