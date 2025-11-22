# pages/5_Analytics.py
import streamlit as st
from app.utils import get_db_conn
import pandas as pd
import plotly.express as px
from app.data.incidents import get_all_incidents

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in")
    st.stop()

conn = get_db_conn()
st.title("📈 Analytics")

try:
    incidents = get_all_incidents()
    if isinstance(incidents, list):
        incidents = pd.DataFrame(incidents)
    if not incidents.empty:
        # severity distribution
        if "severity" in incidents.columns:
            fig = px.histogram(incidents, x="severity", title="Incident severity distribution")
            st.plotly_chart(fig, use_container_width=True)
        # status over time if 'date' column exists
        if "date" in incidents.columns:
            incidents["date"] = pd.to_datetime(incidents["date"])
            counts = incidents.groupby([incidents["date"].dt.to_period("M"), "status"]).size().reset_index(name="count")
            counts["date"] = counts["date"].dt.to_timestamp()
            fig2 = px.line(counts, x="date", y="count", color="status", title="Incidents by status over time")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Not enough data to show charts")
except Exception as e:
    st.error(f"Analytics load failed: {e}")
