import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chatbot import get_chatbot_response

def test_hybrid_translation():
    print("Testing Hybrid Translation System...\n")

    # Test Case 1: Dictionary-based (Should be instant)
    print("Test 1: Dictionary Lookup (Hindi - Greeting)")
    start_time = time.time()
    response_hi = get_chatbot_response("Hello", lang='hi')
    duration = time.time() - start_time
    print(f"Input: 'Hello' | Lang: hi")
    print(f"Response: {response_hi}")
    print(f"Time taken: {duration:.4f}s (Should be very fast)")
    print("-" * 50)

    # Test Case 2: Dynamic Content (Should use Deep Translator)
    # Note: "India" data query will generate a dynamic string like "Total vaccinations in India: X"
    # This is NOT in our dictionary, so it must trigger the translator.
    print("Test 2: Dynamic Data Translation (Hindi - India Stats)")
    start_time = time.time()
    response_dynamic = get_chatbot_response("How many vaccinations in India?", lang='hi')
    duration = time.time() - start_time
    print(f"Input: 'How many vaccinations in India?' | Lang: hi")
    print(f"Response: {response_dynamic}")
    print(f"Time taken: {duration:.4f}s (Should be slower due to API call)")
    print("-" * 50)

    # Test Case 3: French Dynamic
    print("Test 3: Dynamic Data Translation (French - USA Stats)")
    response_fr = get_chatbot_response("vaccinations in USA", lang='fr')
    print(f"Input: 'vaccinations in USA' | Lang: fr")
    print(f"Response: {response_fr}")
    print("-" * 50)

if __name__ == "__main__":
    test_hybrid_translation()
