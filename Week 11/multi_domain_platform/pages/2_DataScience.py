import streamlit as st
import pandas as pd
import plotly.express as px
from multi_domain_platform.data.datasets import (
    get_all_datasets_page,
    add_dataset_page,
    delete_dataset_page
)

st.title("Data Science Module")

if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in first.")
    st.stop()

if st.session_state.user["role"] != "data":
    st.error("Access denied. You are not a database user.")
    st.stop()

datasets = get_all_datasets_page()
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
with st.form("add_dataset"):
    dataset_id = st.text_input("Dataset ID")
    name = st.text_input("Name")
    rows = st.number_input("Rows", min_value=0)
    columns = st.number_input("Columns", min_value=0)
    uploaded_by = st.text_input("Uploaded By")
    upload_date = st.text_input("Upload Date")

    if st.form_submit_button("Add Dataset"):
        add_dataset_page(dataset_id, name, rows, columns, uploaded_by, upload_date)
        st.success("Dataset Added")

if datasets:
    st.subheader("Delete Dataset")
    del_id = st.selectbox("Choose Dataset ID", [d["dataset_id"] for d in datasets])
    if st.button("Delete Dataset"):
        delete_dataset_page(del_id)
        st.success("Dataset Deleted")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.switch_page("home.py")