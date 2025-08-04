# LLM-Agentic-Thinking

A multi-level smart assistant built in Python using the Gemini API, designed to demonstrate structured reasoning, tool-based task solving, and basic agentic behavior across increasing complexity.

---

## 📌 Project Overview

This project implements a command-line AI assistant in three progressive levels:

- **Level 1**: Gemini-powered assistant with structured, step-by-step explanations.
- **Level 2**: Adds a calculator tool to handle arithmetic queries.
- **Level 3**: Agentic assistant capable of using tools (calculator, translator) and reasoning over multi-step tasks.

---

## 🧠 Features by Level

### 🔹 Level 1 – Step-by-Step Gemini Assistant

- Uses Gemini Pro to answer factual questions.
- Enforces a numbered, step-by-step explanation.
- Refuses to solve math problems directly.

**Example Prompts:**

- "What are the colors in a rainbow?"
- "Why is gravity important?"
- "What is 15 + 27?" → Responds with a suggestion to use a calculator

### 🔸 Level 2 – Gemini + Calculator Tool

- Detects arithmetic intent in user input.
- Extracts expressions like "45 + 30" or "12 times 7".
- Performs math using a custom `calculator_tool.py` script.
- Uses Gemini for non-math queries.

**Example Prompts:**

- "Add 45 and 30"
- "What is 12 times 7?"
- "Explain how plants perform photosynthesis"

### 🔺 Level 3 – Full Agentic Assistant with Tool Chaining

- Understands and handles multiple tasks in one prompt.
- Dynamically selects tools based on detected intent:
  - `calculator_tool.py` for math
  - `translation_tool.py` for English → German translation
  - Gemini API for factual reasoning
- Maintains a memory of actions performed per query.

**Example Prompts:**

- "Translate 'Good Morning' to German and then add 20 and 35"
- "What is the capital of Italy and multiply 6 by 4"
- "Translate 'Have a nice day' and tell me why the sky is blue"

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/JoanaPearl-019/LLM.git
```

### 2. Install Dependencies

```bash
pip install google-generativeai
```

### 3. API Key Setup

You need a Gemini API key from [Google AI Studio](https://makersuite.google.com/app). Set the API key as an environment variable:

**On Windows (Command Prompt):**

```bash
set GEMINI_API_KEY=your-api-key-here
```

**On macOS/Linux:**

```bash
export GEMINI_API_KEY=your-api-key-here
```

---

## ▶️ Running the Assistant

### Level 1

```bash
python level1_chatbot.py
```

### Level 2

```bash
python level2_chatbot.py
```

### Level 3

```bash
python full_agent.py
```

---

## 📁 Project Structure

```
LLM-Agentic-Thinking/
├── calculator_tool.py 
├── full history logs.py 
├── full_agent.py 
├── level1_chatbot.py 
├── level_interactions_logs.txt 
├── level2_chatbot.py 
├── level2_interactions.txt 
├── translator_tool.py 
└── README.md
```

---

## 📬 Contact

For questions or contributions, please open an issue or contact the repository maintainer.

