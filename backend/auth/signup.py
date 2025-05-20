import streamlit as st
from backend.utils.hashing import hash_password
import json
import os

USER_DB = "config/user_db.json"


def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)


def signup():
    st.title("Create Account")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        users = load_users()
        if username in users:
            st.warning("Username already exists.")
        else:
            users[username] = hash_password(password)
            save_users(users)
            st.success("Account created! Please log in.")
