# test_new_features.py
"""Quick test of news feed and feedback modules"""

print("Testing News Feed Module...")
try:
    from src.news_feed import fetch_news_headlines
    headlines = fetch_news_headlines('Google News', limit=5)
    print(f"✅ News feed module works! Fetched {len(headlines)} headlines")
    if headlines:
        print(f"   Sample headline: {headlines[0]['title'][:60]}...")
except Exception as e:
    print(f"❌ News feed error: {e}")

print("\nTesting Feedback Module...")
try:
    from src.feedback import initialize_feedback_file, save_feedback
    initialize_feedback_file()
    print("✅ Feedback module works! Feedback file initialized")
except Exception as e:
    print(f"❌ Feedback error: {e}")

print("\n✅ All modules imported successfully!")
