"""
Smart FAQ Chatbot logic using TF-IDF for intent matching.
"""
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.chatbot_knowledge import KNOWLEDGE_BASE

class Chatbot:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.patterns = []
        self.intent_map = []
        self.is_trained = False
        self._train()

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

    def get_response(self, user_input, threshold=0.3):
        """
        Get the best response for the user input.
        
        Args:
            user_input (str): The user's question.
            threshold (float): Minimum similarity score to consider a match.
            
        Returns:
            str: The chatbot's response.
        """
        if not self.is_trained:
            return "I am initializing, please wait a moment."

        # Transform user input
        user_tfidf = self.vectorizer.transform([user_input])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_tfidf, self.tfidf_matrix).flatten()
        
        # Find best match
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score < threshold:
            return "I'm not sure I understand. I am trained to answer questions about COVID-19, vaccines, and symptoms. Could you rephrase that?"
        
        # Get intent
        matched_intent = self.intent_map[best_idx]
        
        # Find response for intent
        for item in KNOWLEDGE_BASE:
            if item['intent'] == matched_intent:
                return random.choice(item['responses'])
        
        return "I'm having trouble retrieving the answer right now."

# Singleton instance
chatbot_instance = Chatbot()

def get_chatbot_response(user_input):
    return chatbot_instance.get_response(user_input)
