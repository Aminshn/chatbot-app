import streamlit as st
import ollama

st.set_page_config(page_title="Test Chatbot", page_icon="💬", layout="centered")
st.title("Chatbot Test")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Input field
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call Ollama
    response = ollama.chat(model="phi3:mini", messages=st.session_state["messages"])

    # Extract model response
    bot_reply = response["message"]["content"]

    # Save assistant message
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
