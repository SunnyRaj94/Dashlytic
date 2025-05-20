import streamlit as st

st.set_page_config(page_title="Dashlytic", layout="wide")

from backend.utils.session_manager import is_logged_in
from frontend.dashboard import show_dashboard
from frontend.login import login
from frontend.signup import signup


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

menu = st.sidebar.selectbox(
    "Menu", ["Login", "Sign Up"] if not is_logged_in() else ["Dashboard"]
)

if is_logged_in():
    show_dashboard()
else:
    if menu == "Login":
        login()
    else:
        signup()
