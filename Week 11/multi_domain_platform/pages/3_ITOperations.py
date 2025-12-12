import streamlit as st
import pandas as pd
import plotly.express as px
from multi_domain_platform.data.tickets import (
    get_all_tickets_page,
    add_ticket_page,
    delete_ticket_page
)

st.title("IT Operations Module")

if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in first.")
    st.stop()

if st.session_state.user["role"] != "it":
    st.error("Access denied. You do not have IT permissions.")
    st.stop()

tickets = get_all_tickets_page()
if tickets:
    df = pd.DataFrame([dict(row) for row in tickets])
    st.dataframe(df, use_container_width=True)

st.subheader("Ticket Status Breakdown")

if not df.empty:
    fig = px.bar(
        df,
        x="status",
        color="status",
        title="Ticket Status Distribution",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No charts available — no ticket data.")
st.subheader("Add Ticket")
with st.form("add_ticket"):
    ticket_id = st.text_input("Ticket ID")
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Description")
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
    assigned_to = st.text_input("Assigned To")
    created_at = st.text_input("Created At")
    resolution_time_hours = st.number_input("Resolution Time (hrs)", min_value=0.0)

    if st.form_submit_button("Add Ticket"):
        add_ticket_page(ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
        st.success("Ticket Added")

if tickets:
    st.subheader("Delete Ticket")
    del_id = st.selectbox("Choose Ticket ID", [t["ticket_id"] for t in tickets])
    if st.button("Delete Ticket"):
        delete_ticket_page(del_id)
        st.success("Ticket Deleted")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.switch_page("home.py")