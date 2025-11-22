# pages/6_Settings.py
import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required")
    st.stop()

st.title("⚙️ Settings")
st.write("Manage account preferences")

if st.button("Reset demo session users"):
    if "users" in st.session_state:
        del st.session_state["users"]
    st.success("Session users cleared")
