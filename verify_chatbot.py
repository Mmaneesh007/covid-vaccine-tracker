import sys
import os

# Add src to path
sys.path.append(os.getcwd())

from src.chatbot import Chatbot

def test_chatbot():
    print("Initializing Chatbot...")
    bot = Chatbot()
    
    print("\n--- Testing Entity Extraction ---")
    queries = [
        "How many vaccinated in India?",
        "Stats for United States",
        "Tell me about Brazil and China"
    ]
    for q in queries:
        entities = bot.extract_entities(q)
        print(f"Query: '{q}' -> Entities: {entities}")

    print("\n--- Testing Dynamic Responses ---")
    test_cases = [
        "How many people are vaccinated in India?",
        "Show me stats for United States",
        "Which country has the most vaccinations?",
        "Is the vaccine safe?", # FAQ fallback
        "What about Brazil?" # Context test (assuming previous query set context, but here we test fresh)
    ]
    
    # Manually set context for the last test
    bot.context['last_country'] = 'Brazil'
    
    for q in test_cases:
        print(f"\nUser: {q}")
        response = bot.get_response(q)
        print(f"Bot: {response}")

if __name__ == "__main__":
    test_chatbot()
