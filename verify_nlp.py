"""
Verify NLP enhancements: spell checking and sentiment analysis
"""
import sys
import os
sys.path.append(os.getcwd())

from src.chatbot import Chatbot

def test_nlp_features():
    print("Initializing Chatbot with NLP features...")
    bot = Chatbot()
    
    print("\n" + "="*60)
    print("TEST 1: Spell Checking")
    print("="*60)
    
    misspelled_queries = [
        "Is the vacine safe?",
        "What are the symptms of covid?",
        "Can I travl after vaccination?",
        "How efectiv is it?"
    ]
    
    for query in misspelled_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
    
    print("\n" + "="*60)
    print("TEST 2: Sentiment Analysis - Negative/Frustrated")
    print("="*60)
    
    negative_queries = [
        "I am so frustrated with this pandemic",
        "This is horrible and I hate it",
        "I'm scared and worried about the vaccine"
    ]
    
    for query in negative_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
    
    print("\n" + "="*60)
    print("TEST 3: Sentiment Analysis - Positive/Happy")
    print("="*60)
    
    positive_queries = [
        "Thank you so much! That is wonderful news!",
        "I'm so happy and excited to get vaccinated!",
        "This is great information, I love it!"
    ]
    
    for query in positive_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
    
    print("\n" + "="*60)
    print("TEST 4: Combined - Misspelling + Sentiment")
    print("="*60)
    
    print(f"\nUser: I'm so worryed about the vacine side efects")
    response = bot.get_response("I'm so worryed about the vacine side efects")
    print(f"Bot: {response}")

if __name__ == "__main__":
    test_nlp_features()
