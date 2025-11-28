"""
Verify emotional intelligence features
"""
import sys
import os
sys.path.append(os.getcwd())

from src.chatbot import Chatbot

def test_emotional_intelligence():
    print("Initializing Chatbot with Emotional Intelligence...")
    bot = Chatbot()
    
    print("\n" + "="*60)
    print("TEST 1: Anger Detection")
    print("="*60)
    
    angry_queries = [
        "I'm angry about this vaccine",
        "This is so frustrating",
        "I hate this pandemic",
        "This information sucks"
    ]
    
    for query in angry_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
    
    print("\n" + "="*60)
    print("TEST 2: Fear/Worry Detection")
    print("="*60)
    
    fear_queries = [
        "I'm scared of getting the vaccine",
        "I'm worried about side effects",
        "I'm anxious about COVID",
        "This makes me so nervous"
    ]
    
    for query in fear_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
    
    print("\n" + "="*60)
    print("TEST 3: Boredom Detection")
    print("="*60)
    
    bored_queries = [
        "This is boring, give me a quick answer",
        "TLDR please",
        "Too long, make it brief",
        "I'm fed up with all this information"
    ]
    
    for query in bored_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
    
    print("\n" + "="*60)
    print("TEST 4: Confusion Detection")
    print("="*60)
    
    confused_queries = [
        "I'm confused about boosters",
        "I don't understand how mRNA works",
        "This is so confusing",
        "Can you clarify the vaccine types?"
    ]
    
    for query in confused_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
    
    print("\n" + "="*60)
    print("TEST 5: Sadness Detection")
    print("="*60)
    
    sad_queries = [
        "I'm so sad about losing loved ones to COVID",
        "I'm depressed because of this pandemic",
        "This makes me upset"
    ]
    
    for query in sad_queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")

if __name__ == "__main__":
    test_emotional_intelligence()
