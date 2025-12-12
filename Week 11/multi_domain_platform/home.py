import streamlit as st
import pandas as pd

from multi_domain_platform.database.users import check_login, create_user

st.set_page_config(page_title="Multi-Domain Intelligence Platform", layout="wide")
st.title("Multi-Domain Intelligence Platform")

# session handling
if "user" not in st.session_state:
    st.session_state.user = None

# AUTHENTICATION PAGE
if st.session_state.user is None:
    st.subheader("User Authentication")
    mode = st.radio("Choose Mode", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["cyber", "data", "it"])

    # register
    if mode == "Register":
        if st.button("Register"):
            create_user(username, password, role)
            st.success("User registered successfully. Please login.")

    # login
    if mode == "Login":
        if st.button("Login"):
            user = check_login(username, password)
            if user:
                st.session_state.user = dict(user)
                st.rerun()
            else:
                st.error("Invalid credentials")

else:
    username = st.session_state.user["username"]
    role = st.session_state.user["role"]

    st.sidebar.success(f"Logged in as: {username} ({role})")

    # ROLE-BASED PAGE ACCESS
    if role == "cyber":
        allowed_pages = ["Cybersecurity", "AI Assistant"]
    elif role == "data":
        allowed_pages = ["Data Science", "AI Assistant"]
    elif role == "it":
        allowed_pages = ["IT Operations", "AI Assistant"]
    else:
        allowed_pages = ["AI Assistant"]

    page = st.sidebar.selectbox("Select Domain", allowed_pages)

    if page == "Cybersecurity":
        st.switch_page("pages/1_Cybersecurity.py")
    elif page == "Data Science":
        st.switch_page("pages/2_DataScience.py")
    elif page == "IT Operations":
        st.switch_page("pages/3_ITOperations.py")
    elif page == "AI Assistant":
        st.switch_page("pages/4_AIAssistant.py")

