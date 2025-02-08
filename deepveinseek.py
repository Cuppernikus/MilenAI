import os
import openai


# Set up OpenRouter API
API_KEY = os.getenv("OPENROUTER_API_KEY")  # ✅ Make sure to set this variable!

if not API_KEY:
    raise ValueError("❌ ERROR: API key not found! Make sure OPENROUTER_API_KEY is set.")

# Initialize OpenRouter client
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# Function to chat with DeepSeek AI via OpenRouter
def chat_with_nurse_ai(user_input):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",  # ✅ Using DeepSeek via OpenRouter
            extra_headers={
                "HTTP-Referer": "https://your-site-url.com",  # Optional
                "X-Title": "DeepVeinSeek",  # Optional
            },
            messages=[
                {"role": "system", "content": "You are DeepVeinSeek, an AI assistant for nurses."},
                {"role": "user", "content": user_input},
            ]
        )

        # Debugging output
        print("📡 DEBUG: Full API Response:", response)

        return response.choices[0].message.content

    except Exception as e:
        print("❌ ERROR: OpenRouter API call failed!", str(e))
        return "Sorry, I encountered an issue while processing your request."

# Simple interactive test
if __name__ == "__main__":
    print("\n🩸 Welcome to DeepVeinSeek! Now powered by OpenRouter! Ask me anything about nursing.")
    
    while True:
        user_query = input("\nAsk DeepVeinSeek: ")
        
        # Exit condition
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Goodbye! Stay awesome, nurse!")
            break
        
        response = chat_with_nurse_ai(user_query)
        print("\n🩸 DeepVeinSeek Says:", response)




