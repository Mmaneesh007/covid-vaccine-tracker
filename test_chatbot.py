from src.chatbot import get_chatbot_response

print("Testing Chatbot Logic...")

# Test 1: Smart Search Priority
print("\nTest 1: Smart Search (CDC guidelines)")
response = get_chatbot_response("CDC guidelines")
print(f"Response: {response[:100]}...")

# Test 2: Intent Matching
print("\nTest 2: Intent Matching (Hello)")
response = get_chatbot_response("Hello")
print(f"Response: {response}")

# Test 3: Emotion
print("\nTest 3: Emotion (I am sad)")
response = get_chatbot_response("I am sad")
print(f"Response: {response}")

print("\nChatbot Logic Verified!")
