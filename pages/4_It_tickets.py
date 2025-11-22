import streamlit as st
from app.utils import get_db_conn
from app.data.tickets import get_all_tickets, insert_ticket, update_ticket_status, delete_ticket
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to Login"):
        st.experimental_set_query_params(page="home")
    st.stop()

st.title("🎫 IT Tickets")

# CREATE form
with st.form("new_ticket"):
    st.subheader("Add new ticket")
    ticket_id = st.text_input("Enter Ticket ID", value="")
    desc = st.text_input("Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
    assigned = st.text_input("Assigned to", value="")
    created=st.text_input("Created Date", value="")
    resolved=st.text_input("Resolved time in hours", value="")
    submitted = st.form_submit_button("Add Ticket")
    if submitted and ticket_id:
        try:
            conn = get_db_conn()
            insert_ticket(ticket_id, priority, desc, status,assigned, created, resolved)
            conn.close()
            st.success("Ticket added")
        except Exception as e:
            st.error(f"Insert failed: {e}")

st.divider()

# READ - Display
st.subheader("All tickets")
try:
    tickets_df = get_all_tickets()
    if isinstance(tickets_df, list):
        tickets_df = pd.DataFrame(tickets_df)
    st.dataframe(tickets_df, use_container_width=True)
except Exception as e:
    st.error(f"Load error: {e}")

# UPDATE / DELETE
# UPDATE / DELETE
st.subheader("Update or delete a ticket")
try:
    if not tickets_df.empty:
        ids = tickets_df["id"].tolist() if "id" in tickets_df.columns else tickets_df.index.tolist()
        sel = st.selectbox("Select ticket id", ids)
        row = tickets_df[tickets_df["id"] == sel].iloc[0] if "id" in tickets_df.columns else tickets_df.loc[sel]

        with st.form("update_ticket"):
            new_status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Closed","Resolved"],
                index=["Open","In Progress","Closed","Resolved"].index(row.get("status","Open"))
            )
            upd = st.form_submit_button("Update")
            if upd:
                try:
                    conn = get_db_conn()
                    update_ticket_status(conn, sel, new_status)
                    conn.close()
                    st.success("Updated")

                except Exception as e:
                    st.error(f"Update failed: {e}")

        if st.button("Delete selected ticket"):
            try:
                conn = get_db_conn()
                delete_ticket(conn, sel)
                conn.close()
                st.success("Deleted")

            except Exception as e:
                st.error(f"Delete failed: {e}")
    else:
        st.info("No tickets to update")
except Exception as e:
    st.error(f"Prepare update/delete failed: {e}")