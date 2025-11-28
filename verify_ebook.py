from src.chatbot import get_chatbot_response

def verify_ebook_knowledge():
    test_queries = [
        "What is NIV?",
        "Does garlic cure COVID?",
        "Can mosquitoes spread COVID?",
        "Is eating chicken safe?",
        "Do thermal scanners work?",
        "How does soap kill virus?",
        "What is ARDS?"
    ]
    
    print("--- Verifying eBook Knowledge ---")
    for query in test_queries:
        response = get_chatbot_response(query)
        print(f"User: {query}")
        # Handle unicode safely for Windows console
        print(f"Bot:  {response.encode('ascii', 'ignore').decode('ascii')}")
        print("-" * 30)

if __name__ == "__main__":
    verify_ebook_knowledge()
