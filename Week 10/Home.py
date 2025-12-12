import streamlit as st
import pandas as pd
import plotly.express as px
# data imports
from app.data.users import check_login, create_user
from app.data.incidents import get_all_incidents, add_incident, delete_incident
from app.data.datasets import get_all_datasets, add_dataset, delete_dataset
from app.data.tickets import get_all_tickets, add_ticket, delete_ticket

# ai import
from app.ai.ai_service import ask_ai

# Streamlit config
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

# DASHBOARD
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

    # CYBERSECURITY (CYBER ROLE ONLY)
    if page == "Cybersecurity":

        if role != "cyber":
            st.error("You do not have permission to access this page.")
            st.stop()

        st.header("Cybersecurity Incidents")

        incidents = get_all_incidents()
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

        with st.form("add_incident_form"):
            incident_id = st.text_input("Incident ID")
            timestamp = st.text_input("Timestamp")
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            category = st.text_input("Category")
            status = st.selectbox("Status", ["Open", "Investigating", "Resolved"])
            description = st.text_area("Description")

            if st.form_submit_button("Add Incident"):
                add_incident(incident_id, timestamp, severity, category, status, description)
                st.success("Incident added")
                st.rerun()

        if incidents:
            st.subheader("Delete Incident")
            del_id = st.selectbox("Select Incident ID", [row["incident_id"] for row in incidents])
            if st.button("Delete Incident"):
                delete_incident(del_id)
                st.success("Incident deleted")
                st.rerun()

    # DATA SCIENCE (DATA ROLE ONLY)
    elif page == "Data Science":

        if role != "data":
            st.error("You do not have permission to access this page.")
            st.stop()

        st.header("Datasets Metadata")

        datasets = get_all_datasets()
        if datasets:
            df = pd.DataFrame([dict(row) for row in datasets])
            st.dataframe(df, use_container_width=True)

        # charts (Plotly)
        import plotly.express as px

        st.subheader("Dataset Size (Rows vs Columns)")

        if not df.empty:
            fig = px.scatter(
                df,
                x="rows",
                y="columns",
                color="uploaded_by",
                size="rows",
                hover_name="name",
                title="Dataset Dimensions",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data for charts.")

        st.subheader("Add Dataset")

        with st.form("add_dataset_form"):
            dataset_id = st.text_input("Dataset ID")
            name = st.text_input("Dataset Name")
            rows = st.number_input("Rows", min_value=0)
            columns = st.number_input("Columns", min_value=0)
            uploaded_by = st.text_input("Uploaded By")
            upload_date = st.text_input("Upload Date")

            if st.form_submit_button("Add Dataset"):
                add_dataset(dataset_id, name, rows, columns, uploaded_by, upload_date)
                st.success("Dataset added")
                st.rerun()

        if datasets:
            st.subheader("Delete Dataset")
            del_id = st.selectbox("Select Dataset ID", [row["dataset_id"] for row in datasets])
            if st.button("Delete Dataset"):
                delete_dataset(del_id)
                st.success("Dataset deleted")
                st.rerun()

    # IT OPERATIONS (IT ROLE ONLY)
    elif page == "IT Operations":

        if role != "it":
            st.error("You do not have permission to access this page.")
            st.stop()

        st.header("IT Support Tickets")

        tickets = get_all_tickets()
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

        with st.form("add_ticket_form"):
            ticket_id = st.text_input("Ticket ID")
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            description = st.text_area("Description")
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            assigned_to = st.text_input("Assigned To")
            created_at = st.text_input("Created At")
            resolution_time_hours = st.number_input("Resolution Hours", min_value=0.0)

            if st.form_submit_button("Add Ticket"):
                add_ticket(ticket_id, priority, description, status,
                           assigned_to, created_at, resolution_time_hours)
                st.success("Ticket added")
                st.rerun()

        if tickets:
            st.subheader("Delete Ticket")
            del_id = st.selectbox("Select Ticket ID", [row["ticket_id"] for row in tickets])
            if st.button("Delete Ticket"):
                delete_ticket(del_id)
                st.success("Ticket deleted")
                st.rerun()

    # AI ASSISTANT (ACCESS FOR ALL)
    elif page == "AI Assistant":
        st.header("AI Assistant")
        prompt = st.text_area("Ask the AI anything:")

        if st.button("Ask AI"):
            if prompt.strip() == "":
                st.error("Please enter a question.")
            else:
                answer = ask_ai(prompt)
                st.subheader("AI Response:")
                st.write(answer)

    # LOGOUT
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
