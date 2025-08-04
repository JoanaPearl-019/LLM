import google.generativeai as genai
import os
import re
from datetime import datetime
from calculator_tool import calculate
from translator_tool import translate_to_german

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

LOG_FILE = "level3_interactions.txt"

# Log all interactions
def log_interaction(user_input, response):
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
        log.write(f"You: {user_input}\n")
        log.write(f"Assistant: {response}\n")
        log.write("-" * 50 + "\n")

# Detect translation requests
def find_translation(text):
    match = re.search(r'translate\s+[\'"](.+?)[\'"]\s+(?:into\s+)?german', text.lower())
    return match.group(1) if match else None

# Detect math operations
def find_calculations(text):
    text = text.lower()
    expressions = []

    # Natural language: Add X and Y
    for match in re.finditer(r'add (\d+) and (\d+)', text):
        expressions.append(f"{match.group(1)} + {match.group(2)}")

    for match in re.finditer(r'multiply (\d+) and (\d+)', text):
        expressions.append(f"{match.group(1)} * {match.group(2)}")

    # Math-like pattern
    expressions += re.findall(r'(\d+\s*[\+\-\*/]\s*\d+)', text)
    return expressions

# Detect general LLM info queries
def is_llm_question(text):
    keywords = ["capital", "distance", "largest", "who is", "what is"]
    return any(k in text.lower() for k in keywords)

def ask_gemini(user_input):
    prompt = f"You are a helpful assistant. Answer clearly.\nUser: {user_input}\nAssistant:"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {e}"

# Main agent loop
def main():
    print("🔴 Gemini Agentic Assistant (Level 3)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response_parts = []

        # 1. Handle translation
        phrase = find_translation(user_input)
        if phrase:
            translation = translate_to_german(phrase)
            response_parts.append(f"Translated '{phrase}' to German: {translation}")

        # 2. Handle math expressions
        expressions = find_calculations(user_input)
        for expr in expressions:
            result = calculate(expr)
            response_parts.append(f"{expr.strip()} = {result}")

        # 3. Handle general knowledge
        if is_llm_question(user_input):
            llm_response = ask_gemini(user_input)
            response_parts.append(f"LLM Answer: {llm_response}")

        # If nothing matched, fallback to Gemini
        if not response_parts:
            fallback = ask_gemini(user_input)
            response_parts.append(fallback)

        final_response = "\n".join(response_parts)
        print(f"Assistant:\n{final_response}\n")
        log_interaction(user_input, final_response)

if __name__ == "__main__":
    main()