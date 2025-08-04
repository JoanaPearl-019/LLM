from googletrans import Translator

def translate_to_german(text):
    translator = Translator()
    try:
        result = translator.translate(text, dest='de')
        return result.text
    except Exception as e:
        return f"Translation error: {str(e)}"

# ✅ TEST BLOCK (must be at bottom)
if __name__ == "__main__":
    user_text = input("Enter text to translate to German: ")
    translation = translate_to_german(user_text)
    print("Translated:", translation)
