import google.generativeai as genai
import os
import re
from datetime import datetime
from calculator_tool import calculate

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Log file
LOG_FILE = "level2_interactions.txt"

# Detect math-related query
def is_math_query(text):
    keywords = r"\b(add|plus|sum|subtract|minus|difference|multiply|times|product|divide|divided|multiplied|added)\b"
    symbols = r"\d+\s*[\+\-\*/]\s*\d+"
    return bool(re.search(f"{keywords}|{symbols}", text.lower()))

# Detect multi-step compound question
def is_multi_step(text):
    return any(joiner in text.lower() for joiner in [" and also ", " then ", " as well as ", " in addition ", " and tell me ", " also tell me "])

# Convert natural language math query to Python expression
def extract_expression(text):
    text = text.lower().strip()

    # Handle "Add 45 and 30"
    match = re.search(r"(?:add|plus|added)\s+(\d+)\s+(?:and|to)\s+(\d+)", text)
    if match:
        return f"{match.group(1)} + {match.group(2)}"

    # Handle "Multiply 9 and 8" or "9 times 8"
    match = re.search(r"(?:multiply|times|multiplied)\s+(\d+)\s+(?:and|by)?\s*(\d+)", text)
    if match:
        return f"{match.group(1)} * {match.group(2)}"

    match = re.search(r"(\d+)\s+(?:times|multiplied by)\s+(\d+)", text)
    if match:
        return f"{match.group(1)} * {match.group(2)}"

    # Handle "Subtract 5 from 10"
    match = re.search(r"(?:subtract|minus)\s+(\d+)\s+from\s+(\d+)", text)
    if match:
        return f"{match.group(2)} - {match.group(1)}"

    # Handle direct math expressions: 45 + 30
    expr = re.search(r"(\d+\s*[\+\-\*/]\s*\d+)", text)
    return expr.group(1) if expr else None

# Ask Gemini for general queries
def ask_gemini(user_input):
    prompt = f"You are a helpful assistant. Answer step-by-step.\nUser: {user_input}\nAssistant:"
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

# Log interaction
def log_interaction(user_input, assistant_response):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            log.write(f"You: {user_input}\n")
            log.write(f"Assistant: {assistant_response}\n")
            log.write("-" * 50 + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

# Main CLI loop
def main():
    print("🟡 Gemini Assistant with Calculator Tool (Level 2)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        if is_multi_step(user_input):
            answer = "Graceful failure (no multi-step yet)"
        elif is_math_query(user_input):
            expression = extract_expression(user_input)
            if expression:
                answer = calculate(expression)
            else:
                answer = "Sorry, I can only handle one step at a time right now."
        else:
            answer = ask_gemini(user_input)

        print(f"Assistant:\n{answer}\n")
        log_interaction(user_input, answer)

if __name__ == "__main__":
    main()