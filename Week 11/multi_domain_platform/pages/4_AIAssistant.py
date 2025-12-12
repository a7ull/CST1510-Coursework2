import streamlit as st
from multi_domain_platform.data.ai_service import ask_ai_page

st.title("AI Assistant")

if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in first.")
    st.stop()

prompt = st.text_area("Ask the AI anything")

if st.button("Ask"):
    if not prompt.strip():
        st.error("Enter a question.")
    else:
        answer = ask_ai_page(prompt)
        st.subheader("AI Response:")
        st.write(answer)