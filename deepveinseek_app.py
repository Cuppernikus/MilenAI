import streamlit as st
import openai

# Retrieve API key from Streamlit Secrets
API_KEY = st.secrets["general"].get("OPENROUTER_API_KEY", None)

# UI title
st.title("🩸 DeepVeinSeek - Your AI Nursing Assistant")
st.markdown("Ask me anything about nursing! I can provide **clinical guidance, nursing best practices, and patient care tips.** 🏥")

# Stop execution if API key is missing
if not API_KEY:
    st.error("⚠️ **API key not found!** Please check your configuration in Streamlit Secrets.")
    st.stop()

# Initialize OpenAI client with OpenRouter API
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.text_input("💬 **Ask DeepVeinSeek a question:**", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send request to OpenRouter API
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

        with st.chat_message("assistant"):
            st.markdown(ai_response)

    except Exception as e:
        st.error(f"❌ ERROR: OpenRouter API call failed! {e}")




