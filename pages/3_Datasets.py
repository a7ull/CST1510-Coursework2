import streamlit as st
from app.utils import get_db_conn
from app.data.datasets import get_all_datasets, insert_dataset, update_dataset_name, delete_dataset
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to Login"):
        st.experimental_set_query_params(page="home")
    st.stop()

st.title("Datasets")

# CREATE form
with st.form("new_dataset"):
    st.subheader("Add new dataset")
    name = st.text_input("Dataset Name")
    drows = st.text_input("Number of rows")
    dcols = st.text_input("Number of columns")
    uploaded=st.text_input("Uploaded By:")
    upl_dated=st.text_input("Uploaded Date:")
    submitted = st.form_submit_button("Add Dataset")
    if submitted and name:
        try:
            conn = get_db_conn()
            insert_dataset(name, drows, dcols, uploaded, upl_dated)
            conn.close()
            st.success("Dataset added")
        except Exception as e:
            st.error(f"Insert failed: {e}")

st.divider()

# READ - Display
st.subheader("All datasets")
try:
    datasets_df = get_all_datasets()
    if isinstance(datasets_df, list):
        datasets_df = pd.DataFrame(datasets_df)
    st.dataframe(datasets_df, use_container_width=True)
except Exception as e:
    st.error(f"Load error: {e}")

# UPDATE / DELETE
st.subheader("Update or delete a dataset")
try:
    if not datasets_df.empty:
        ids = datasets_df["id"].tolist() if "id" in datasets_df.columns else datasets_df.index.tolist()
        sel = st.selectbox("Select dataset id", ids)
        row = datasets_df[datasets_df["id"] == sel].iloc[0] if "id" in datasets_df.columns else datasets_df.loc[sel]

        with st.form("update_dataset"):
            new_name = st.text_input("Name", value=row.get("name", ""))
            upd = st.form_submit_button("Update")
            if upd:
                try:
                    conn = get_db_conn()
                    update_dataset_name(conn, sel,new_name)
                    conn.commit()
                    conn.close()
                    st.success("Updated")

                except Exception as e:
                    st.error(f"Update failed: {e}")

        if st.button("Delete selected dataset"):
            try:
                conn = get_db_conn()
                delete_dataset(conn, sel)
                conn.commit()
                conn.close()
                st.success("Deleted")

            except Exception as e:
                st.error(f"Delete failed: {e}")
    else:
        st.info("No datasets to update")
except Exception as e:
    st.error(f"Prepare update/delete failed: {e}")