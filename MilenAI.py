import streamlit as st
import openai
import random
import time

# ---------------------------------------------------------------------------
# Page configuration (must be first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MilenAI - Clinical Intelligence",
    page_icon="\u2695\ufe0f",
    layout="centered",
)

# ---------------------------------------------------------------------------
# API configuration
# ---------------------------------------------------------------------------
# Supports both Groq and OpenAI backends. Set the appropriate key in
# .streamlit/secrets.toml under [general].
#
#   [general]
#   GROQ_API_KEY  = "gsk_..."
#   OPENAI_API_KEY = "sk-..."
# ---------------------------------------------------------------------------

_secrets = st.secrets.get("general", {})
GROQ_KEY = _secrets.get("GROQ_API_KEY")
OPENAI_KEY = _secrets.get("OPENAI_API_KEY")

if GROQ_KEY:
    client = openai.OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")
    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    ADVANCED_MODEL = "llama-3.3-70b-versatile"
elif OPENAI_KEY:
    client = openai.OpenAI(api_key=OPENAI_KEY)
    DEFAULT_MODEL = "gpt-4o-mini"
    ADVANCED_MODEL = "gpt-4-turbo"
else:
    st.error("No API key found. Add GROQ_API_KEY or OPENAI_API_KEY to .streamlit/secrets.toml")
    st.stop()

# ---------------------------------------------------------------------------
# System prompt — defines MilenAI's clinical educator persona
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are MilenAI, an expert AI-powered clinical educator and nursing assistant. "
        "You provide evidence-based, concise answers grounded in peer-reviewed clinical "
        "guidelines. When answering NCLEX-style questions, clearly identify the correct "
        "answer and explain the rationale. Always remind users that your answers do not "
        "replace professional medical advice."
    ),
}

# ---------------------------------------------------------------------------
# Topic-based quick questions
# ---------------------------------------------------------------------------
TOPIC_QUESTIONS = {
    "Medication": [
        "What are the 5 rights of medication administration?",
        "How do you calculate medication dosages?",
        "What are common side effects of beta-blockers?",
        "Explain the difference between ACE inhibitors and ARBs.",
    ],
    "Cardiology": [
        "What are priority interventions for a patient in heart failure?",
        "How do you recognize and manage atrial fibrillation?",
        "What ECG changes indicate myocardial infarction?",
        "Explain the use of beta-blockers in hypertension management.",
    ],
    "Respiratory": [
        "How do you interpret arterial blood gases (ABGs)?",
        "What are nursing interventions for COPD patients?",
        "What is the difference between BiPAP and CPAP?",
        "How do you assess for impending respiratory failure?",
    ],
    "Endocrine": [
        "Explain the difference between DKA and HHS.",
        "What are priority nursing actions for a hypoglycemic patient?",
        "How does insulin affect potassium levels?",
        "Discuss patient education for newly diagnosed Type 2 diabetes.",
    ],
    "Critical Care": [
        "What are signs and symptoms of sepsis?",
        "How do you assess for shock?",
        "What are the criteria for SIRS vs. sepsis?",
        "What are key components of ventilator management?",
    ],
}

# Keywords that route to the advanced model (NCLEX-style questions)
NCLEX_KEYWORDS = ["nclex", "exam", "priority", "best action", "intervention", "answer choices"]

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Helper — choose model based on query content
# ---------------------------------------------------------------------------
def _pick_model(query: str) -> str:
    if any(kw in query.lower() for kw in NCLEX_KEYWORDS):
        return ADVANCED_MODEL
    return DEFAULT_MODEL


def get_ai_response(messages: list[dict], model: str) -> str:
    """Call the configured LLM backend with retry logic."""
    full_messages = [SYSTEM_PROMPT] + messages
    # Keep conversation context manageable (last 20 exchanges)
    if len(full_messages) > 41:
        full_messages = [SYSTEM_PROMPT] + full_messages[-40:]

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=full_messages,
                temperature=0.2,
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
            else:
                return f"Sorry, I could not get a response. Error: {e}"

# ---------------------------------------------------------------------------
# UI — Header
# ---------------------------------------------------------------------------
st.title("MilenAI — Clinical Intelligence")
st.caption("Your AI-Powered Clinical Educator & Assistant")
st.divider()

# ---------------------------------------------------------------------------
# UI — Sidebar with quick questions and info
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Quick Questions")
    st.markdown("Select a topic and click a question to get started.")

    topic = st.selectbox("Topic", list(TOPIC_QUESTIONS.keys()))
    questions = TOPIC_QUESTIONS[topic]

    for q in questions:
        if st.button(q, key=f"qq_{q}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            model = _pick_model(q)
            with st.spinner("Thinking..."):
                answer = get_ai_response(st.session_state.messages, model)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    st.divider()

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown(
        "**About MilenAI**\n\n"
        "Evidence-based clinical answers powered by advanced AI. "
        "Designed for nurses, nursing students, and healthcare professionals."
    )
    st.caption(
        "This tool is for educational purposes only. "
        "It does not replace professional medical advice, diagnosis, or treatment. "
        "Always consult a qualified healthcare provider."
    )

# ---------------------------------------------------------------------------
# UI — Chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# UI — Chat input (anchored at bottom, enter-to-submit)
# ---------------------------------------------------------------------------
if user_input := st.chat_input("Ask MilenAI a clinical question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    model = _pick_model(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_response = get_ai_response(st.session_state.messages, model)
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# ---------------------------------------------------------------------------
# UI — Footer disclaimer
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "MilenAI is an AI-based educational assistant and does not replace "
    "professional medical advice. Your conversations are processed by a "
    "third-party AI service — do not enter protected health information (PHI)."
)
