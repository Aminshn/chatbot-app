import streamlit as st
import redis
import json
import ollama
import uuid  # for unique session IDs

# Connect to Redis
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# --- Session ID input ---
input_session_id = st.text_input("Enter session ID (leave empty for new session):")

# Initialize session_id
if "session_id" not in st.session_state:
    if input_session_id.strip():  # use input if provided
        st.session_state["session_id"] = input_session_id.strip()
    else:
        st.session_state["session_id"] = str(uuid.uuid4())
else:
    # If input box has a value different from current, update session_id
    if input_session_id.strip() and input_session_id.strip() != st.session_state["session_id"]:
        st.session_state["session_id"] = input_session_id.strip()

session_id = st.session_state["session_id"]
st.text(f"Current session ID: {session_id}")


# Functions to get/save messages in Redis
def get_messages(session_id):
    messages_json = r.get(session_id)
    if messages_json:
        return json.loads(messages_json)
    return []

def save_messages(session_id, messages):
    r.set(session_id, json.dumps(messages), ex=3600)

# Streamlit page setup
st.set_page_config(page_title="Test Chatbot", page_icon="💬", layout="centered")
st.title("Chatbot Test")
st.text(session_id)

# Load messages from Redis
messages = get_messages(session_id)
st.session_state["messages"] = messages

# User input
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

    # Save updated messages to Redis
    save_messages(session_id, st.session_state["messages"])

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
