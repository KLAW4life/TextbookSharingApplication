import streamlit as st
import authn
from duo_universal.client import Client, DuoException
from streamlit_javascript import st_javascript


def nav_to(url):
  nav_script = """
      <meta http-equiv="refresh" content="0; url='%s'">
  """ % (url)
  st.write(nav_script, unsafe_allow_html=True)

def TFA(username):
  duo_client = Client(
      client_id="",
      client_secret="",
      host="",
      redirect_uri= st_javascript("window.location.origin") + "/main"
  )
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
    st.success(f"Welcome {st.session_state['username']}")
    TFA(st.session_state["username"])
    placeholder.empty()
  else:
    st.success("Welcome guest")

else:
  st.error("Not authenticated")