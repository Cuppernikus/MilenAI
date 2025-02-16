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
client = openai.OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

def get_ai_response(messages):
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # ✅ Correct model name for Groq
        messages=messages
    )
    st.write("🔍 Response Source:", response.model)  # Debug: Confirm it's from Groq
    return response.choices[0].message.content

st.title("MilenAI - Your AI-Powered Clinical Assistant 🩺")
st.markdown("**Providing fast, evidence-based insights for nurses and healthcare professionals.**")


# 💬 Chat Input Field
user_input = st.text_input(
    "💬 **Ask MilenAI a clinical question:**",
    key="user_input",
    placeholder="Type your question here and press Enter...",
)
# Sidebar for quick access
with st.sidebar:
    st.title("⚡ Quick Access")
    st.markdown("🚀 **Shortcuts:**")
    if st.button("📊 Trending NCLEX Questions"):
        st.session_state.user_input = "What are the most commonly asked NCLEX questions?"
    if st.button("💡 Medication Safety Guide"):
        st.session_state.user_input = "What are the 5 rights of medication administration?"
    st.divider()
    st.markdown("🔹 **About MilenAI:**")
    st.write("MilenAI is an AI-powered clinical assistant designed to help nurses with real-world patient care and NCLEX prep.")

#Preset buttons for user input
st.subheader("💡 Quick Questions")
preset_questions = [
    "What are the 5 rights of medication administration?",
    "How do you interpret ABGs (arterial blood gases)?",
    "What are priority nursing interventions for a patient in shock?",
    "Explain the difference between DKA and HHS.",
    "What are the most commonly asked NCLEX questions?"
]

for question in preset_questions:
    if st.button(question):
        user_input = question  # Automatically fills the input field

# Store chat history
if "messages" not in st.session_state:
    for msg in reversed(st.session_state.messages):  # Newest at bottom
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(f"<div style='background-color:#D0E8FF; padding:10px; border-radius:10px;'>🗨️ **You:** {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color:#D4EDDA; padding:10px; border-radius:10px;'>👩‍⚕️ **Nurse AI:** {msg['content']}</div>", unsafe_allow_html=True)

# Auto-scroll to the latest message
st.markdown("<div id='latest-message'></div>", unsafe_allow_html=True)
st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)


# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f"🗨️ **You:** {msg['content']}")
        else:
            st.markdown(f"🩺 **MilenAI:** {msg['content']}")

# 🛠️ Optimized API Call with Groq
def get_ai_response(messages, retries=3, delay=2):
    """Send a request to Groq API with retry logic."""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages
            )
            return response.choices[0].message.content  # ✅ Success
        except Exception as e:
            st.warning(f"⚠️ Groq API failed (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)  # ⏳ Wait before retrying
    return "⚠️ Sorry, I couldn’t get a response from Groq after multiple attempts. Please try again later."

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response with retry handling
    ai_response = get_ai_response(st.session_state.messages)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
      
    #Display AI Chat beautifully
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(f"<div style='background-color:#D0E8FF; padding:10px; border-radius:10px;'>🗨️ **You:** {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color:#D4EDDA; padding:10px; border-radius:10px;'>👩‍⚕️ **Nurse AI:** {msg['content']}</div>", unsafe_allow_html=True)


# ✨ Footer
st.divider()
st.markdown(
        "⚠️ _This is an AI-based assistant and does not replace professional medical advice._"
)

#Analytics tracker 
import pandas as pd

if "query_count" not in st.session_state:
    st.session_state.query_count = {}

if user_input:
    st.session_state.query_count[user_input] = st.session_state.query_count.get(user_input, 0) + 1

# Display the most asked questions
if st.session_state.query_count:
    st.subheader("🔥 Trending Nursing Questions")
    df = pd.DataFrame(st.session_state.query_count.items(), columns=["Question", "Count"]).sort_values(by="Count", ascending=False)
    st.dataframe(df)








