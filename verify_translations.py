import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chatbot import get_chatbot_response

def test_translations():
    test_cases = [
        ("Hello", "en"),
        ("Hello", "hi"),
        ("Hello", "bn"),
        ("Hello", "fr"),
        ("Is the vaccine safe?", "hi"),
        ("Is the vaccine safe?", "ta"),
        ("I am angry", "hi"),  # Test empathy translation
        ("I am angry", "fr"),
    ]

    print("Testing Chatbot Translations...\n")

    for input_text, lang in test_cases:
        print(f"Input: '{input_text}' | Language: {lang}")
        response = get_chatbot_response(input_text, lang=lang)
        print(f"Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    test_translations()
