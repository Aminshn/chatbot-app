import streamlit as st
import redis
import json
import ollama
import uuid

# Connect to Redis
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# --- Get all saved sessions ---
def list_sessions():
    keys = r.keys("chat:*")  # all chat sessions
    return [k.split("chat:")[1] for k in keys]

# --- Auto-generate or reuse session ID ---
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

# Dropdown to select existing session
saved_sessions = list_sessions()
selected_session = st.sidebar.selectbox(
    "Select a saved session ID:", 
    options=["(new session)"] + saved_sessions,
    index=0
)

# If user picks an old session → load it
if selected_session != "(new session)":
    st.session_state["session_id"] = selected_session
else:
    # generate a fresh one
    st.session_state["session_id"] = str(uuid.uuid4())

session_id = st.session_state["session_id"]
redis_key = f"chat:{session_id}"

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("Multi-user Chatbot")
st.caption(f"Session: {session_id}")


# --- Helper functions ---
def get_messages(session_id):
    msgs = r.lrange(f"chat:{session_id}", 0, -1)  # get full list
    return [json.loads(m) for m in msgs]

def add_message(session_id, role, content):
    r.rpush(f"chat:{session_id}", json.dumps({"role": role, "content": content}))
    r.expire(f"chat:{session_id}", 3600)  # optional TTL (1h)


messages = get_messages(session_id)

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user msg
    add_message(session_id, "user", user_input)

    # Call Ollama
    response = ollama.chat(model="phi3:mini", messages=get_messages(session_id))
    bot_reply = response["message"]["content"]

    # Save assistant msg
    add_message(session_id, "assistant", bot_reply)

# Display chat history
for msg in get_messages(session_id):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
