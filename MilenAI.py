import streamlit as st
import openai
import time

# Retrieve API key from Streamlit Secrets
API_KEY = st.secrets["general"].get("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", None)

# Stop execution if API key is missing
if not API_KEY:
    st.error("❌ ERROR: API key not found! Please check Streamlit Secrets.")
    st.stop()

# Initialize OpenAI client using Groq API
client = openai.Client(
    api_key=API_KEY,
    base_url="https://api.groq.com/v1"  # Ensure correct Groq API base URL
)

# 🎨 UI Enhancements
st.set_page_config(page_title="MilenAI - Clinical Intelligence", page_icon="⚕️")
st.title("⚕️ MilenAI - Clinical Intelligence")
st.markdown(
    "### 💬 Ask me anything about clinical practice, nursing, and patient care!\n"
    "**MilenAI is powered by cutting-edge AI, created and managed by a healthcare innovator.** 🚀"
)
st.divider()

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
    "**MilenAI is an advanced AI platform, created and managed by a healthcare innovator.**\n"
    "⚠️ _This is an AI-based assistant and does not replace professional medical advice._"
)




