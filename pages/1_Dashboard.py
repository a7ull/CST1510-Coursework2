
import streamlit as st
from app.utils import get_db_conn
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets

# Page guard
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to Login"):
        st.experimental_set_query_params(page="home")
    st.stop()

conn = get_db_conn()

st.title("📊 Dashboard")
st.success(f"Welcome, {st.session_state.username}!")

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    try:
        incidents = get_all_incidents()
        st.metric("Incidents", len(incidents))
    except Exception:
        st.metric("Incidents", "N/A")

with col2:
    try:
        datasets = get_all_datasets()
        st.metric("Datasets", len(datasets))
    except Exception:
        st.metric("Datasets", "N/A")

with col3:
    try:
        tickets = get_all_tickets()
        st.metric("IT Tickets", len(tickets))
    except Exception:
        st.metric("IT Tickets", "N/A")

st.markdown("---")
st.subheader("Quick Views")
colA, colB = st.columns(2)

with colA:
    st.write("Recent incidents (top 10)")
    try:
        df_inc = get_all_incidents()
        st.dataframe(df_inc.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"Error loading incidents: {e}")

with colB:
    st.write("Datasets (top 10)")
    try:
        df_ds = get_all_datasets()
        st.dataframe(df_ds.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"Error loading datasets: {e}")

st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.success("Logged out")

