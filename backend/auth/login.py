import streamlit as st
from backend.utils.hashing import verify_password
from backend.utils.session_manager import login_user
import json
import os

USER_DB = "config/user_db.json"


def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}


def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        users = load_users()
        if username in users and verify_password(password, users[username]):
            login_user(username)
            st.success(f"Welcome {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials.")
