import os
import time
import streamlit as st
import openai
import pandas as pd

# ✅ Load API Key from Streamlit Secrets
API_KEY = st.secrets["general"]["GROQ_API_KEY"]

if not API_KEY:
    st.error("❌ ERROR: API key not found! Please check Streamlit Secrets.")
    st.stop()

# ✅ Initialize OpenAI client with Groq
client = openai.OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

def get_ai_response(messages, retries=3, delay=2):
    """Send a request to Groq API with retry logic."""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            st.warning(f"⚠️ Groq API failed (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)
    return "⚠️ Sorry, I couldn’t get a response from Groq after multiple attempts. Please try again later."

# 🏥 **Header & Title**
st.markdown("<h1 style='text-align: center;'>🩺 MilenAI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4CAF50;'>Your AI-Powered Clinical Assistant</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Helping Nurses & Students with Instant Evidence-Based Answers</h4>", unsafe_allow_html=True)

# 💬 **Chat Input Field**
user_input = st.text_input("💬 **Ask MilenAI a clinical question:**", key="user_input")
if user_input:
    response = get_ai_response([{"role": "user", "content": user_input}])
    st.write("👩‍⚕️ **MilenAI:**", response)

# 🔹 **Quick Access Preset Questions**
st.subheader("💡 Quick Questions")
preset_questions = [
    "What are the 5 rights of medication administration?",
    "How do you interpret ABGs (arterial blood gases)?",
    "What are priority nursing interventions for a patient in shock?",
    "Explain the difference between DKA and HHS."
]

for question in preset_questions:
    if st.button(question):
        user_input = question  # Autofill user input

# 💾 **Chat History Storage**
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🏥 **Display Chat Messages**
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f"<div style='background-color:#D0E8FF; padding:10px; border-radius:10px;'>🗨️ **You:** {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:#D4EDDA; padding:10px; border-radius:10px;'>👩‍⚕️ **MilenAI:** {msg['content']}</div>", unsafe_allow_html=True)

# 💬 **Process AI Response & Update Chat History**
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    ai_response = get_ai_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# 🔥 **Analytics Tracker - Most Asked Questions**
if "query_count" not in st.session_state:
    st.session_state.query_count = {}

if user_input:
    st.session_state.query_count[user_input] = st.session_state.query_count.get(user_input, 0) + 1

if st.session_state.query_count:
    st.subheader("📊 Trending Nursing Questions")
    df = pd.DataFrame(st.session_state.query_count.items(), columns=["Question", "Count"]).sort_values(by="Count", ascending=False)
    st.dataframe(df)

# ⚠️ **Disclaimer Footer**
st.divider()
st.markdown(
        "⚠️ _This is an AI-based assistant and does not replace professional medical advice._"
)
