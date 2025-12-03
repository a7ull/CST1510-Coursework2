import streamlit as st
from google import genai

client = genai.Client(api_key="AIzaSyBylCS0Ilz2WgSV3ncDQy8b8qWI-1N6FLI")
st.title("GEMINI AI")

# Define session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper function similar to your OpenAI example
def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# Display historical chat
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

# Chat input
prompt = st.chat_input("Hello, how can I help you today?")

if prompt:
    # Add user message
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    ai_reply = ask_ai(prompt)

    # Add assistant message
    st.session_state.messages.append(("assistant", ai_reply))
    with st.chat_message("assistant"):
        st.markdown(ai_reply)