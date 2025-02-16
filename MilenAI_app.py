import os
import time
import streamlit as st
import openai


API_KEY = st.secrets["general"]["GROQ_API_KEY"]  # ✅ This should match secrets.toml
  # ✅ Ensure this matches secrets.toml

if not API_KEY:
    st.error("❌ ERROR: API key not found! Please check Streamlit Secrets.")
    st.stop()


# ✅ Initialize OpenAI client with Groq
client = openai.Client(api_key=API_KEY, base_url="https://api.groq.com/v1")

def get_ai_response(messages):
    response = client.chat.completions.create(
        model="groq/gpt-4-turbo",  
        messages=messages
    )
    st.write("🔍 Response Source:", response.model)  # Debug: Confirm it's from Groq
    return response.choices[0].message.content

st.title("MilenAI - Now Powered by Groq! 🚀")

user_input = st.text_input("Ask MilenAI a question:")

if user_input:
    response = get_ai_response([{"role": "user", "content": user_input}])
    st.write("🩺 MilenAI:", response)

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🛠️ Optimized API Call with Groq
def get_ai_response(messages, retries=3, delay=2):
    """Send a request to Groq API with optimized handling and retry logic."""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="groq/gpt-4-turbo",  # Adjust if necessary for available Groq models
                messages=messages
            )
            return response.choices[0].message.content  # ✅ Success
        except Exception as e:
            st.warning(f"⚠️ Groq API failed (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)  # ⏳ Wait before retrying
    return "⚠️ Sorry, I couldn’t get a response from Groq. Please try again later."

# 💬 Chat Input Field
user_input = st.text_input("💬 **Ask MilenAI a clinical question:**", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response with retry handling
    ai_response = get_ai_response(st.session_state.messages)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Display AI response beautifully
    with st.chat_message("assistant"):
        st.markdown(f"🩺 **MilenAI:** {ai_response}")

# ✨ Footer
st.divider()
st.markdown(
        "⚠️ _This is an AI-based assistant and does not replace professional medical advice._"
)








