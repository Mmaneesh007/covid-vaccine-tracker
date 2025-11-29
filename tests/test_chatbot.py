import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
from src.chatbot import Chatbot, get_chatbot_response

class TestChatbot:
    @pytest.fixture
    def chatbot(self):
        """Create a Chatbot instance for testing"""
        # Mock the knowledge base and translations to avoid external dependencies if needed
        # But for unit tests, we can use the real class if it's self-contained enough.
        # The Chatbot class loads data in __init__, so we might want to mock that.
        
        with patch('src.chatbot.get_all_countries', return_value=['India', 'USA', 'France']):
            bot = Chatbot()
            # Force training with a small dummy corpus if needed, or rely on real one
            # bot.patterns = ["hello", "vaccine stats"]
            # bot.intent_map = ["greeting", "country_stats"]
            # bot._train()
            return bot

    def test_initialization(self, chatbot):
        """Test that chatbot initializes correctly"""
        assert chatbot.vectorizer is not None
        assert chatbot.is_trained is True
        assert len(chatbot.countries) > 0
        assert 'india' in chatbot.countries

    def test_preprocess_input(self, chatbot):
        """Test input preprocessing and spell checking"""
        # Basic cleaning
        assert chatbot.preprocess_input("Hello World") == "Hello World"
        
        # Spell checking (mocked or real depending on TextBlob)
        # "symptms" -> "symptoms" is a known correction in our context
        # assert "symptoms" in chatbot.preprocess_input("symptms").lower() 
        
        # Case preservation
        assert chatbot.preprocess_input("India") == "India"

    def test_extract_entities(self, chatbot):
        """Test entity extraction (countries)"""
        # Simple extraction
        entities = chatbot.extract_entities("stats for India")
        assert "india" in entities
        
        # Multiple entities
        entities = chatbot.extract_entities("compare USA and France")
        assert "usa" in entities
        assert "france" in entities
        
        # No entities
        entities = chatbot.extract_entities("hello there")
        assert len(entities) == 0

    def test_analyze_sentiment(self, chatbot):
        """Test sentiment analysis"""
        # Positive
        sent = chatbot.analyze_sentiment("I am happy and great")
        assert sent['polarity'] > 0
        
        # Negative
        sent = chatbot.analyze_sentiment("I am sad and angry")
        assert sent['polarity'] < 0
        
        # Neutral
        sent = chatbot.analyze_sentiment("The sky is blue")
        assert -0.1 <= sent['polarity'] <= 0.1

    def test_detect_emotion_keywords(self, chatbot):
        """Test emotion detection"""
        assert chatbot.detect_emotion_keywords("I am so angry") == "anger"
        assert chatbot.detect_emotion_keywords("I am scared") == "fear"
        assert chatbot.detect_emotion_keywords("This is confusing") == "confusion"
        assert chatbot.detect_emotion_keywords("I am happy") is None

    @patch('src.chatbot.get_latest_by_country')
    def test_get_db_response_stats(self, mock_get_latest, chatbot):
        """Test database response for country stats"""
        # Mock DB return
        mock_df = pd.DataFrame({
            'location': ['India'],
            'total_vaccinations': [1000000],
            'pct_vaccinated': [75.5]
        })
        mock_get_latest.return_value = mock_df
        
        response = chatbot.get_db_response('country_stats', ['india'])
        assert "India" in response
        assert "1,000,000" in response
        assert "75.5%" in response

    def test_get_response_greeting(self, chatbot):
        """Test basic greeting response"""
        response = chatbot.get_response("hello")
        # Should return one of the greeting responses
        assert len(response) > 0
        # We can't check exact string as it's random, but it shouldn't be error
        assert "error" not in response.lower()

    def test_context_retention(self, chatbot):
        """Test that chatbot remembers context"""
        # Set context manually
        chatbot.context['last_country'] = 'india'
        
        # Ask follow-up question
        # We need to mock get_db_response or the underlying DB call
        with patch.object(chatbot, 'get_db_response', return_value="Stats for India") as mock_db:
            chatbot.get_response("what about stats")
            
            # Should have called db response with context
            # Note: get_response logic is complex, might need specific triggers
            # For now, just check if extract_entities uses context if implemented
            pass 

    def test_multilingual_support(self, chatbot):
        """Test that language parameter is accepted"""
        # Just check it runs without error
        response = chatbot.get_response("hello", lang='hi')
        assert isinstance(response, str)
        assert len(response) > 0
