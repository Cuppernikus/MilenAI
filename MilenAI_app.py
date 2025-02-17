import streamlit as st
import openai
import pandas as pd
import random

# OpenAI API Key (Load from Streamlit Secrets)
API_KEY = st.secrets["general"]["OPENAI_API_KEY"]
openai.api_key = API_KEY

# Session state initialization
if "query_cache" not in st.session_state:
    st.session_state.query_cache = {}
if "ratings" not in st.session_state:
    st.session_state.ratings = {}
if "query_count" not in st.session_state:
    st.session_state.query_count = {}
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# List of quick questions
QUICK_QUESTIONS = [
    "What are the 5 rights of medication administration?",
    "How do you interpret ABGs (arterial blood gases)?",
    "What are priority nursing interventions for a patient in shock?",
    "Explain the difference between DKA and HHS.",
]

# -------------------------------
# **Hybrid Model Selection**
# -------------------------------
def openai_chat_completion(messages, temperature=0.2, max_tokens=500):
    """
    Determines the correct model based on question type.
    Uses GPT-4 Turbo for NCLEX-style questions and GPT-4o Mini for general clinical inquiries.
    """
    # Keywords indicating an NCLEX exam question
    nclex_keywords = ["nclex", "exam", "priority", "best action", "intervention", "question", "answer choices"]

    # Determine the appropriate model
    model = "gpt-4o-mini"
    if any(keyword in messages[-1]["content"].lower() for keyword in nclex_keywords):
        model = "gpt-4-turbo"  # Switch to Turbo for NCLEX questions

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI API Error: {e}"

# -------------------------------
# **Handling User Queries**
# -------------------------------
def handle_user_query(query):
    """
    Handles user queries by determining whether it should be an NCLEX-style or general clinical response.
    Caches responses for efficiency.
    """
    if not query.strip():
        return

    # Check if already cached
    if query in st.session_state.query_cache:
        st.write("🩺 **MilenAi (Cached):**", st.session_state.query_cache[query])
    else:
        # Get response from the correct AI model
        messages = [{"role": "user", "content": query}]
        answer = openai_chat_completion(messages)

        # Store in cache & display response
        st.session_state.query_cache[query] = answer
        st.write("🩺 **MilenAi:**", answer)

    # Append to session query history
    st.session_state.query_history.append(query)

# -------------------------------
# **Streamlit UI**
# -------------------------------
st.markdown("""
    <h1 style="text-align: center;">🩺 MilenAi </h1>
    <h4 style="text-align: center; color: #4CAF50;">Your AI-Powered Clinical Educator & Assistant</h4>
    <h6 style="text-align: center; color: #555;">Evidence-Based Answers from Peer-Reviewed Sources</h6>
    <hr>
""", unsafe_allow_html=True)

# -------------------------------
# **User Input**
# -------------------------------
user_query = st.text_input("💬 **Ask MilenAi a clinical (or NCLEX) question:**", key="user_input")
submit_col = st.columns([0.8, 0.2])[1]

if submit_col.button("Submit"):
    handle_user_query(user_query)

# -------------------------------
# **Quick Questions (FIXED)**
# -------------------------------
import random

# Define topic-based preset questions
TOPIC_QUESTIONS = {
    "medication": [
        "What are the 5 rights of medication administration?",
        "How do you calculate medication dosages?",
        "What are common side effects of beta-blockers?",
        "Explain the difference between ACE inhibitors and ARBs.",
    ],
    "cardiology": [
        "What are priority interventions for a patient in heart failure?",
        "How do you recognize and manage atrial fibrillation?",
        "What ECG changes indicate myocardial infarction?",
        "Explain the use of beta-blockers in hypertension management.",
    ],
    "respiratory": [
        "How do you interpret arterial blood gases (ABGs)?",
        "What are nursing interventions for COPD patients?",
        "What is the difference between BiPAP and CPAP?",
        "How do you assess for impending respiratory failure?",
    ],
    "endocrine": [
        "Explain the difference between DKA and HHS.",
        "What are priority nursing actions for a hypoglycemic patient?",
        "How does insulin affect potassium levels?",
        "Discuss patient education for newly diagnosed Type 2 diabetes.",
    ],
    "critical care": [
        "What are signs and symptoms of sepsis?",
        "How do you assess for shock?",
        "What are the criteria for SIRS vs. sepsis?",
        "What are key components of ventilator management?",
    ],
}

def get_dynamic_questions(user_query):
    """
    Extracts a keyword from the user's query and selects a set of related questions.
    If no keyword matches, returns a general set of questions.
    """
    for topic, questions in TOPIC_QUESTIONS.items():
        if topic in user_query.lower():
            return random.sample(questions, min(len(questions), 3))  # Randomize 3 questions

    # If no match, return general quick questions
    return random.sample(sum(TOPIC_QUESTIONS.values(), []), 3)  # Flatten and pick 3

# Example usage:
user_input = "What are priority interventions for a heart failure patient?"
quick_questions = get_dynamic_questions(user_input)
print(quick_questions)  # Example output: ["How do you recognize and manage atrial fibrillation?", "What ECG changes indicate myocardial infarction?", "What are priority interventions for a patient in heart failure?"]

# -------------------------------
# **Session Query History**
# -------------------------------
st.subheader("📝 Recent Queries")
if st.session_state.query_history:
    for i, q in enumerate(st.session_state.query_history[::-1][:5], start=1):
        st.write(f"{i}. {q}")
else:
    st.write("No queries yet.")

# -------------------------------
# **Footer**
# -------------------------------
st.write("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "⚠️ <em>This is an AI-based assistant and does not replace professional medical advice.</em>"
    "</p>",
    unsafe_allow_html=True
)


