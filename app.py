import streamlit as st

st.title("💬 My Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Your message:")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    # TODO: send to LLM + memory

# Display chat
for msg in st.session_state["messages"]:
    st.write(f"**{msg['role']}:** {msg['content']}")
