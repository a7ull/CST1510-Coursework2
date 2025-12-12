import streamlit as st
import pandas as pd
import plotly.express as px
from multi_domain_platform.data.incidents import (
    get_all_incidents_page,
    add_incident_page,
    delete_incident_page
)

st.title("Cybersecurity Module")

if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in first.")
    st.stop()

if st.session_state.user["role"] != "cyber":
    st.error("Access denied. You do not have Cybersecurity permissions.")
    st.stop()

incidents = get_all_incidents_page()
if incidents:
    df = pd.DataFrame([dict(row) for row in incidents])
    st.dataframe(df, use_container_width=True)
st.subheader("Severity Distribution")

if not df.empty:
    fig = px.bar(
        df,
        x="severity",
        title="Incident Severity Distribution",
        color="severity",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data for charts.")

st.subheader("Add Incident")
with st.form("add_incident"):
    incident_id = st.text_input("Incident ID")
    timestamp = st.text_input("Timestamp")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    category = st.text_input("Category")
    status = st.selectbox("Status", ["Open", "Investigating", "Resolved"])
    description = st.text_area("Description")

    if st.form_submit_button("Add Incident"):
        add_incident_page(incident_id, timestamp, severity, category, status, description)
        st.success("Incident Added")

if incidents:
    st.subheader("Delete Incident")
    del_id = st.selectbox("Choose Incident", [i["incident_id"] for i in incidents])
    if st.button("Delete Incident"):
        delete_incident_page(del_id)
        st.success("Incident Deleted")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.switch_page("home.py")