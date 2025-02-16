import streamlit as st
import openai
import time

# Retrieve API key from Streamlit Secrets
API_KEY = st.secrets["general"].get("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", None)

# Stop execution if API key is missing
if not API_KEY:
    st.error("❌ ERROR: API key not found! Please check Streamlit Secrets.")
    st.stop()

# Initialize OpenAI client with OpenRouter API
client = openai.Client(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# 🎨 Beautiful UI Design
st.set_page_config(page_title="DeepVeinSeek - AI Clinical Assistant", page_icon="🩸")
st.title("🩸 DeepVeinSeek - AI Clinical Assistant")
st.markdown(
    "### 💬 Ask me anything about nursing and patient care!\n"
    "**DeepVeinSeek is an AI chatbot created and managed by a Registered Nurse** 🏥\n"
    "_⚠️ Disclaimer: This is an AI chatbot, not a licensed healthcare provider. Always verify information with clinical guidelines._"
)
st.divider()

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🛠️ Function to handle OpenRouter API calls with retry logic
def get_ai_response(messages, retries=3, delay=3):
    """Send a request to OpenRouter API with retries in case of failure."""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=messages
            )
            return response.choices[0].message.content  # ✅ Success
        except Exception as e:
            st.warning(f"⚠️ OpenRouter API failed (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)  # ⏳ Wait before retrying
    return "⚠️ Sorry, I couldn’t get a response from OpenRouter. Please try again later."

# 💬 Chat Input Field
user_input = st.text_input("💬 **Ask DeepVeinSeek a clinical question:**", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response with retry handling
    ai_response = get_ai_response(st.session_state.messages)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Display AI response beautifully
    with st.chat_message("assistant"):
        st.markdown(f"🩺 **DeepVeinSeek:** {ai_response}")

# ✨ Footer
st.divider()
st.markdown(
    "**DeepVeinSeek is an AI chatbot created and managed by a Registered Nurse.**\n"
    "⚠️ _This is an AI-based assistant and does not replace professional medical advice._"
)







