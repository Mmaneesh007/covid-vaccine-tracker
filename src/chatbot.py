"""
Smart FAQ Chatbot logic using TF-IDF for intent matching and dynamic DB querying.
"""
import random
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from src.chatbot_knowledge import KNOWLEDGE_BASE
from src.storage import get_all_countries, get_latest_by_country, get_country_timeseries

class Chatbot:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.patterns = []
        self.intent_map = []
        self.is_trained = False
        self.countries = []
        self.context = {}  # Store last queried entity
        self._train()
        self._load_data()

    def _load_data(self):
        try:
            self.countries = [c.lower() for c in get_all_countries()]
            print(f"Loaded {len(self.countries)} countries for entity extraction.")
        except Exception as e:
            print(f"Error loading countries: {e}")
            self.countries = []

    def preprocess_input(self, text):
        """
        Preprocess and correct spelling mistakes in user input.
        Uses a conservative approach to avoid over-correction.
        """
        try:
            # Split into words and check each
            words = text.split()
            corrected_words = []
            
            for word in words:
                # Only try to correct alphabetic words (skip punctuation, numbers)
                if word.isalpha() and len(word) > 2:
                    word_blob = TextBlob(word.lower())
                    corrected = str(word_blob.correct())
                    
                    # Only apply correction if it's different and reasonable
                    if corrected != word.lower() and len(corrected) >= len(word) - 1:
                        # Preserve original capitalization
                        if word[0].isupper():
                            corrected = corrected.capitalize()
                        corrected_words.append(corrected)
                        if corrected.lower() != word.lower():
                            print(f"Spell check: '{word}' -> '{corrected}'")
                    else:
                        corrected_words.append(word)
                else:
                    corrected_words.append(word)
            
            return ' '.join(corrected_words)
        except Exception as e:
            print(f"Spell check error: {e}")
            return text

    def analyze_sentiment(self, text):
        """
        Analyze sentiment of user input.
        Returns: dict with 'polarity' (-1 to 1) and 'subjectivity' (0 to 1)
        """
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment
            return {
                'polarity': sentiment.polarity,
                'subjectivity': sentiment.subjectivity
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {'polarity': 0.0, 'subjectivity': 0.0}

    def detect_emotion_keywords(self, text):
        """
        Detect specific emotions based on keywords.
        Returns: emotion type ('anger', 'fear', 'boredom', 'confusion', 'sadness', None)
        """
        text_lower = text.lower()
        
        # Define emotion keyword dictionaries
        emotions = {
            'anger': ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'frustrated', 'hate', 'sucks', 'infuriating'],
            'fear': ['scared', 'afraid', 'terrified', 'frightened', 'worried', 'nervous', 'anxious', 'fear'],
            'boredom': ['bored', 'boring', 'too long', 'tldr', 'too much', 'short answer', 'quick', 'brief', 'fed up', 'tired'],
            'confusion': ['confused', "don't understand", 'confusing', 'not clear', 'unclear', 'lost', "don't get", 'clarify'],
            'sadness': ['sad', 'depressed', 'down', 'upset', 'crying', 'devastated', 'heartbroken', 'miserable', 'unhappy']
        }
        
        # Check for emotions (in priority order)
        for emotion, keywords in emotions.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return emotion
        
        return None

    def _train(self):
        """
        Train the TF-IDF vectorizer on the knowledge base patterns.
        """
        corpus = []
        for item in KNOWLEDGE_BASE:
            intent = item['intent']
            for pattern in item['patterns']:
                corpus.append(pattern)
                self.patterns.append(pattern)
                self.intent_map.append(intent)
        
        # Fit the vectorizer
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.is_trained = True

    def extract_entities(self, user_input):
        """
        Extract known entities (countries) from user input.
        """
        found_entities = []
        user_lower = user_input.lower()
        
        # Simple string matching for countries
        # Sort countries by length (desc) to match "United States" before "United"
        for country in sorted(self.countries, key=len, reverse=True):
            if country in user_lower:
                found_entities.append(country)
                # Remove found country to avoid double matching substrings
                user_lower = user_lower.replace(country, "")
                
        return found_entities

    def get_db_response(self, intent, entities):
        """
        Generate a response based on database queries.
        """
        print(f"DEBUG: get_db_response intent={intent} entities={entities}")
        if not entities:
            # Check context
            if 'last_country' in self.context:
                entities = [self.context['last_country']]
            else:
                if intent == 'country_stats':
                    return "Which country are you asking about?"

        country_name = entities[0] if entities else None
        # Capitalize for display (simple heuristic, or fetch from DB again if needed)
        display_name = country_name.title() if country_name else ""
        
        try:
            if intent == 'country_stats':
                df = get_latest_by_country(limit=1000) # Get all to find specific
                # Filter in memory for now, or use specific query
                # Better to use get_country_timeseries or specific query if we had one for single country latest
                # Re-using get_latest_by_country efficiently
                row = df[df['location'].str.lower() == country_name]
                
                if row.empty:
                    return f"I don't have data for {display_name}."
                
                data = row.iloc[0]
                total = int(data['total_vaccinations']) if pd.notnull(data['total_vaccinations']) else 0
                pct = data['pct_vaccinated'] if pd.notnull(data['pct_vaccinated']) else 0
                
                self.context['last_country'] = country_name
                return f"In {data['location']}, {total:,} doses have been administered ({pct:.1f}% vaccinated)."

            elif intent == 'top_countries':
                df = get_latest_by_country(limit=5)
                response = "Top 5 countries by vaccination rate:\n"
                for i, row in df.iterrows():
                    response += f"{i+1}. {row['location']}: {row['pct_vaccinated']:.1f}%\n"
                return response

        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Sorry, I encountered an error querying the data: {str(e)}"

        return "I'm not sure how to answer that data question."

    def get_response(self, user_input, threshold=0.3):
        """
        Get the best response for the user input.
        """
        if not self.is_trained:
            return "I am initializing, please wait a moment."

        # 0. Spell check and sentiment analysis
        corrected_input = self.preprocess_input(user_input)
        sentiment = self.analyze_sentiment(corrected_input)
        emotion = self.detect_emotion_keywords(corrected_input)

        # 1. Check for specific data keywords + entities
        entities = self.extract_entities(corrected_input)
        user_lower = corrected_input.lower()
        
        data_intents = {
            'country_stats': ['how many', 'stats', 'vaccination', 'vaccinated', 'doses', 'status', 'rate', 'what about', 'how about'],
            'top_countries': ['top', 'best', 'highest', 'most vaccinated', 'most vaccinations']
        }

        # Check for top countries
        if any(keyword in user_lower for keyword in data_intents['top_countries']):
            return self.get_db_response('top_countries', [])

        # Check for country stats
        if entities or ('last_country' in self.context and any(k in user_lower for k in ['what about', 'and'])):
             # If explicit data keywords present, use DB.
             if any(keyword in user_lower for keyword in data_intents['country_stats']):
                 return self.get_db_response('country_stats', entities)

        # 2. If emotion detected, prioritize emotional intents
        if emotion:
            # Map emotions to their corresponding intent names
            emotion_intent_map = {
                'anger': 'feeling_angry',
                'fear': 'feeling_scared',
                'boredom': 'feeling_bored',
                'confusion': 'feeling_confused',
                'sadness': 'feeling_sad'
            }
            
            target_intent = emotion_intent_map.get(emotion)
            
            if target_intent:
                # Find the response for this emotional intent
                for item in KNOWLEDGE_BASE:
                    if item['intent'] == target_intent:
                        response = random.choice(item['responses'])
                        return self._add_empathy(response, sentiment, emotion)
        
        # 3. Fallback to TF-IDF for other intents
        user_tfidf = self.vectorizer.transform([corrected_input])
        similarities = cosine_similarity(user_tfidf, self.tfidf_matrix).flatten()
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score < threshold:
            # If low score but we have an entity, maybe try stats?
            if entities:
                 response = self.get_db_response('country_stats', entities)
            else:
                response = "I'm not sure I understand. I am trained to answer questions about COVID-19, vaccines, and symptoms. Could you rephrase that?"
        else:
            matched_intent = self.intent_map[best_idx]
            
            # Find response for intent
            response = None
            for item in KNOWLEDGE_BASE:
                if item['intent'] == matched_intent:
                    response = random.choice(item['responses'])
                    break
            
            if not response:
                response = "I'm having trouble retrieving the answer right now."
        
        # 4. Add empathetic prefix/suffix based on sentiment and emotion
        return self._add_empathy(response, sentiment, emotion)

    def _add_empathy(self, response, sentiment, emotion=None):
        """
        Add empathetic tone to response based on user's sentiment and detected emotion.
        """
        # If specific emotion keyword detected, prioritize that
        if emotion:
            emotion_prefixes = {
                'anger': "I understand your frustration. ",
                'fear': "It's natural to feel worried. Let me help ease your concerns. ",
                'boredom': "I'll keep this brief. ",
                'confusion': "Let me explain this more clearly. ",
                'sadness': "I'm sorry you're going through this. "
            }
            prefix = emotion_prefixes.get(emotion, "")
            if prefix:
                return prefix + response
        
        # Otherwise, use sentiment polarity
        polarity = sentiment['polarity']
        
        # Negative/Frustrated (polarity < -0.3)
        if polarity < -0.3:
            empathy_prefix = "I'm sorry to hear you're feeling that way. "
            return empathy_prefix + response
        
        # Positive/Happy (polarity > 0.5)
        elif polarity > 0.5:
            return response + " Glad to help!"
        
        # Neutral or slightly emotional
        else:
            return response

# Singleton instance
chatbot_instance = Chatbot()

def get_chatbot_response(user_input):
    return chatbot_instance.get_response(user_input)
