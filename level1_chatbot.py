import google.generativeai as genai
import os
import re
from datetime import datetime

# Set your Gemini API key securely using an environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model (1.5 flash recommended)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Output log file
LOG_FILE = "level1_interactions.txt"

# Step-by-step enforced prompt
STEP_BY_STEP_PROMPT = """
You are a helpful assistant. Always respond in a clear, step-by-step explanation.

Rules:
- Do not use acronyms like ROYGBIV or just list things without explaining.
- Explain the answer logically in 2–6 steps.
- If the question is a math problem (e.g., 'What is 15 + 23?'), DO NOT solve it.
  Instead, respond: "I'm not able to solve math directly. You may use a calculator tool for that."

Now answer this user query step by step:
"""

# Detect basic math questions to refuse solving
def is_math_query(text):
    symbols = r"\d+\s*[\+\-\*/]\s*\d+"
    keywords = r"\b(add|plus|sum|subtract|minus|multiply|times|product|divide|divided|total)\b"
    return bool(re.search(f"{keywords}|{symbols}", text.lower()))

# Ask Gemini, applying prompt and logic
def ask_gemini(user_input):
    if is_math_query(user_input):
        return "I'm not able to solve math directly. You may use a calculator tool for that."

    prompt = STEP_BY_STEP_PROMPT + f"\nUser: {user_input}\nAssistant:"
    try:
        response = model.generate_content(prompt)
        if hasattr(response, "text"):
            return response.text.strip()
        elif hasattr(response, "candidates"):
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return str(response)
    except Exception as e:
        return f"Gemini error: {e}"

# Save interactions to file
def log_interaction(user_input, assistant_response):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            log.write(f"You: {user_input}\n")
            log.write(f"Assistant: {assistant_response}\n")
            log.write("-" * 50 + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

# Main program loop
def main():
    print("🔹 Gemini Smart Assistant (Level 1)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break

        answer = ask_gemini(user_input)
        print(f"Assistant:\n{answer}\n")
        log_interaction(user_input, answer)

if __name__ == "__main__":
    main()