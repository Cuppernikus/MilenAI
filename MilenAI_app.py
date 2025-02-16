import os
import time
import streamlit as st
import openai
import pandas as pd

# ✅ Load API Key from Streamlit Secrets
API_KEY = st.secrets["general"]["OPENAI_API_KEY"]

if not API_KEY:
    st.error("❌ ERROR: API key not found! Please check Streamlit Secrets.")
    st.stop()

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=API_KEY)

# ✅ Corrected AI Response Function (Only One Version!)
def get_ai_response(messages, retries=3, delay=2):
    """Send a request to OpenAI API with retry logic and dynamic model selection."""
    
    # Default to GPT-4o Mini for general use
    model_name = "gpt-4o-mini"

    # Switch to GPT-4 Turbo for NCLEX-style or complex medical queries
    if any(keyword in messages[-1]["content"].lower() for keyword in ["nclex", "exam", "priority intervention", "practice test"]):
        model_name = "gpt-4-turbo"

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            return response.choices[0].message.content  # ✅ Success
        except Exception as e:
            st.warning(f"⚠️ OpenAI API failed (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)  # ⏳ Wait before retrying

    return "⚠️ Sorry, I couldn’t get a response from OpenAI after multiple attempts. Please try again later."

# 🎨 **Custom Styling for UI**
st.markdown("""
    <style>
        .stTextInput {
            text-align: center;
            font-size: 16px;
            padding: 10px;
        }
        div.stButton > button {
            background-color: #007BFF;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# 🏥 **App Header**
st.markdown("""
    <h1 style="text-align: center;">🩺 MilenAI</h1>
    <h4 style="text-align: center; color: #4CAF50;">Your AI-Powered Clinical Assistant</h4>
    <h6 style="text-align: center;">Helping Nurses & Students with Instant Evidence-Based Answers</h6>
""", unsafe_allow_html=True)

# 💬 **Chat Input Field**
user_input = st.text_input("💬 **Ask MilenAI a clinical question:**", key="user_input")

if user_input:
    # Get AI response with retry handling
    ai_response = get_ai_response([{"role": "user", "content": user_input}])

    # Display AI response beautifully
    st.markdown(f"<div style='background-color:#D4EDDA; padding:10px; border-radius:10px;'>👩‍⚕️ **MilenAI:** {ai_response}</div>", unsafe_allow_html=True)

# 💡 **Quick Question Presets**
st.subheader("💡 Quick Questions")
preset_questions = [
    "What are the 5 rights of medication administration?",
    "How do you interpret ABGs (arterial blood gases)?",
    "What are priority nursing interventions for a patient in shock?",
    "Explain the difference between DKA and HHS."
]

# Handle preset question clicks
preset_clicked = st.radio("Choose a question:", preset_questions, index=None, key="preset")

if preset_clicked:
    ai_response = get_ai_response([{"role": "user", "content": preset_clicked}])
    st.markdown(f"<div style='background-color:#D4EDDA; padding:10px; border-radius:10px;'>👩‍⚕️ **MilenAI:** {ai_response}</div>", unsafe_allow_html=True)

# 📊 **Analytics Tracker**
if "query_count" not in st.session_state:
    st.session_state.query_count = {}

if user_input:
    st.session_state.query_count[user_input] = st.session_state.query_count.get(user_input, 0) + 1

# 🔥 **Trending Nursing Questions**
if st.session_state.query_count:
    st.subheader("🔥 Trending Nursing Questions")
    df = pd.DataFrame(st.session_state.query_count.items(), columns=["Question", "Count"]).sort_values(by="Count", ascending=False)
    st.dataframe(df)

# ✨ **Footer**
st.divider()
st.markdown(
    "⚠️ _This is an AI-based assistant and does not replace professional medical advice._"
)
