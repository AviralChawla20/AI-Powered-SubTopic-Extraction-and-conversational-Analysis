import streamlit as st
import requests

# API Details
API_KEY = "c1e746cb3782b24cc075464e201ccd76"
CONVAI_API_URL = "https://api.convai.com/character/getResponse"

# Character IDs for models
CHARACTER_IDS = {
    "GPT-4O": "8521a5ac-b70e-11ef-bdc4-42010a7be016",
    "Gemini": "3ec90ce6-b702-11ef-b02e-42010a7be016",
    "LLaMA": "c52b777c-b70e-11ef-8df1-42010a7be016",
    "Claude": "ef7b2ab8-b70e-11ef-9045-42010a7be016",
    "Mistral": "37d9b1f8-b70f-11ef-a748-42010a7be016",
}

# Sidebar: Select Model
st.sidebar.title("Select Model")
selected_model = st.sidebar.radio(
    "Choose a model to chat with:", list(CHARACTER_IDS.keys())
)

# Check if model has changed
if "current_model" not in st.session_state:
    st.session_state.current_model = selected_model
if selected_model != st.session_state.current_model:
    st.session_state.current_model = selected_model
    st.session_state.messages = []  # Reset chat history on model switch

st.title("AI-Powered SubTopic Extraction and Conversational Analysis")
st.write(f"Currently chatting with: **{selected_model}**")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # Store chat history as a list of dicts


# Function to call ConvAI API
def call_convai_api(user_message, char_id):
    payload = {
        "userText": user_message,
        "charID": char_id,
        "sessionID": "100",
        "voiceResponse": "False",
    }
    headers = {
        "CONVAI-API-KEY": API_KEY,
    }
    response = requests.post(CONVAI_API_URL, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("text", "No response received")
    else:
        return f"Error: {response.status_code} - {response.text}"


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Type your message here:")
if user_input:
    # Add user's message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Call ConvAI API with the appropriate charID
    char_id = CHARACTER_IDS[selected_model]
    bot_response = call_convai_api(user_input, char_id)

    # Add bot's response to chat history
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    with st.chat_message("bot"):
        st.write(bot_response)
