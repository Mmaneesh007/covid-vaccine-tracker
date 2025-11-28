"""
Test the exact query that failed to verify the fix
"""
import sys
import os
sys.path.append(os.getcwd())

from src.chatbot import Chatbot

def test_bug_fix():
    print("Testing the bug fix...")
    bot = Chatbot()
    
    print("\n" + "="*60)
    print("CRITICAL TEST: The Query That Failed")
    print("="*60)
    
    query = "I am scared to take vaccine"
    print(f"\nUser: {query}")
    response = bot.get_response(query)
    print(f"Bot: {response}")
    
    print("\n" + "="*60)
    print("Additional Fear-Related Queries")
    print("="*60)
    
    queries = [
        "I'm scared of the vaccine",
        "I'm afraid to get vaccinated",
        "I'm worried about getting the shot",
        "I'm nervous about side effects"
    ]
    
    for q in queries:
        print(f"\nUser: {q}")
        response = bot.get_response(q)
        print(f"Bot: {response}")

if __name__ == "__main__":
    test_bug_fix()
