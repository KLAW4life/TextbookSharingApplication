import streamlit as st
import authn
import os
import pickle
from duo_universal.client import Client, DuoException
from streamlit_javascript import st_javascript
from streamlit_extras.switch_page_button import switch_page


def save_session_state():
  try:
    with open('session_state.pkl', 'wb') as f:
      pickle.dump(st.session_state["username"], f)
  except Exception as e:
    st.error("Error during saving session state")


def nav_to(url):
  nav_script = """
      <meta http-equiv="refresh" content="0; url='%s'">
  """ % (url)
  st.write(nav_script, unsafe_allow_html=True)


def TFA(username):
  duo_client = Client(st.secrets["client_id"],
                      st.secrets["client_secret"],
                        st.secrets["host"],
                    redirect_uri=st_javascript("window.location.origin") +
                      "/Home/?embedded=true")
  try:
    duo_client.health_check()
  except DuoException:
    st.error("Duo health check failed")
  state = duo_client.generate_state()
  prompt_uri = duo_client.create_auth_url(username, state)

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
  authn.login_form()

if st.session_state["authenticated"]:
  if st.session_state["username"]:
    save_session_state()
    st.success(f"Welcome {st.session_state['username']}")
    TFA(st.session_state["username"])
    placeholder.empty()
  else:
    del st.session_state["username"]
    st.success("Welcome guest")
    switch_page("main")

else:
  st.error("Not authenticated")
