# pages/2_Incidents.py
import streamlit as st
from app.utils import get_db_conn
from app.data.incidents import get_all_incidents, insert_incident, update_incident_status, delete_incident
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to Login"):
        st.experimental_set_query_params(page="home")
    st.stop()

st.title("🚨 Cyber Incidents")

# CREATE form
with st.form("new_incident"):
    st.subheader("Add new incident")
    timestamp = st.text_input("Date : ", value="")
    intype= st.text_input("Incident Type: ", value="")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
    desc= st.text_input("Incident Description", value="")
    submitted = st.form_submit_button("Add Incident")
    if submitted and timestamp:
        try:
            conn = get_db_conn()
            insert_incident(timestamp, intype, severity, status, desc)
            conn.close()
            st.success("Incident added")

        except Exception as e:
            st.error(f"Insert failed: {e}")

st.divider()

# READ - Display
st.subheader("All incidents")
try:
    incidents_df = get_all_incidents()
    if isinstance(incidents_df, list):
            incidents_df = pd.DataFrame(incidents_df)
    st.dataframe(incidents_df, use_container_width=True)
except Exception as e:
    st.error(f"Load error: {e}")


# UPDATE / DELETE
st.subheader("Update or delete an incident")
try:
    if not incidents_df.empty:
        ids = incidents_df["id"].tolist() if "id" in incidents_df.columns else incidents_df.index.tolist()
        sel = st.selectbox("Select incident id", ids)
        row = incidents_df[incidents_df["id"] == sel].iloc[0] if "id" in incidents_df.columns else incidents_df.loc[sel]

        with st.form("update_incident"):
            new_title = st.text_input("Title", value=row.get("title", ""))
            new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved","Closed"], index=["Open","In Progress","Resolved","Closed"].index(row.get("status","Open")))
            upd = st.form_submit_button("Update")
            if upd:
                try:
                    conn = get_db_conn()
                    update_incident_status(conn, sel,new_status)
                    st.success("Updated")
                    conn.close()
                except Exception as e:
                    st.error(f"Update failed: {e}")


        if st.button("Delete selected incident"):
            try:
                conn = get_db_conn()
                delete_incident(conn, sel)
                st.success("Deleted")
                conn.close()
            except Exception as e:
                st.error(f"Delete failed: {e}")

    else:
        st.info("No incidents to update")
except Exception as e:
    st.error(f"Prepare update/delete failed: {e}")

