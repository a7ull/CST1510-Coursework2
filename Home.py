# Home.py
import streamlit as st
from app.utils import get_db_conn
from app.services.user_service import login_user

st.set_page_config(page_title="Intelligence Platform - Home", layout="wide")

# Initialize session state keys
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

st.title("Intelligence Platform — Login")

conn = get_db_conn()

tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Sign in")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in"):

        ok = False
        role = None
        try:
            res = login_user(login_username,login_password)

            if isinstance(res, tuple):
                ok, role = res
            else:
                ok = bool(res)
        except Exception as e:
            st.error(f"Login error: {e}")
            ok = False

        if ok:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            if role:
                st.session_state.role = role
            st.success("Logged in successfully!")
            st.switch_page("pages/1_Dashboard.py")

        else:
            st.error("Invalid credentials")

with tab_register:
    st.subheader("Create an account")
    register_username = st.text_input("Choose a username", key="register_username")
    register_password = st.text_input("Choose a password", type="password", key="register_password")
    register_confirm = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        if not register_username or not register_password:
            st.warning("Please complete all fields")
        elif register_password != register_confirm:
            st.error("Passwords do not match")
        else:


            if "users" not in st.session_state:
                st.session_state.users = {}
            if register_username in st.session_state.users:
                st.error("Username already exists (session demo)")
            else:
                st.session_state.users[register_username] = register_password
                st.success("Accountcreated — switch to Login tab to sign in")

st.divider()


