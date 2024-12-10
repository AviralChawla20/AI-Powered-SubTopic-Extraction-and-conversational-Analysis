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
        "sessionID": "-1",
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


# Make introductory API call if not done already
char_id = CHARACTER_IDS[selected_model]
intro_prompt = (
    "You are my friend who will answer my questions just like a friend would. "
    "You are an AI trained to read news articles and answer questions in a manner "
    "that feels conversational, human-like, and to the point. Carefully analyze the "
    "content of the news article and answer questions based solely on the information provided.\n\n"
    "Poland signed a $4 billion loan under the United States' foreign military financing program "
    "that will help finance the transformation of its armed forces, the Polish defence minister said on Thursday. "
    "'This is another proof of enormous trust and strong alliance between Poland and the United States of America,' "
    "Wladyslaw Kosiniak-Kamysz posted on X. Kosiniak-Kamysz said that in total the United States has provided Poland "
    "with over $11 billion to finance armament programs, including Patriot air defence systems and Apache helicopters. "
    "Spurred by Russia's full-scale invasion of Ukraine in 2022, Poland became NATO's top spender in terms of the proportion "
    "of its national wealth devoted to defence. Warsaw said it will spend 4.1% of gross domestic product on defense in 2024 "
    "with a pledge to increase this to 4.7% in 2025.\n\n"
    "If a question is unrelated to the article or cannot be answered based on its content, respond in a natural, casual tone, such as: "
    "'I don’t really know about that, to be honest. We were just talking about the news, so maybe stick to that?'"
)
    # call_convai_api(intro_prompt, char_id)

# Display current chat