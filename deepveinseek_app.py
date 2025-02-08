import streamlit as st
import os
import openai

# Set API key from environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("❌ ERROR: API key not found! Make sure OPENROUTER_API_KEY is set.")
    st.stop()

# Initialize OpenAI client with OpenRouter
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# Streamlit UI
st.title("🩸 DeepVeinSeek - Nursing Chatbot")
st.markdown("**Ask me anything about nursing, and I'll help you!**")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.text_input("Ask DeepVeinSeek:", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send request to OpenRouter API (DeepSeek model)
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=st.session_state.messages
        )
        
        ai_response = response.choices[0].message.content

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_response)

    except Exception as e:
        st.error(f"❌ ERROR: OpenRouter API call failed! {e}")

