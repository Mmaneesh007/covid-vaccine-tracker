import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Path to the eBook text
EBOOK_PATH = os.path.join(os.getcwd(), "extracted_ebook_text.txt")
CACHE_PATH = os.path.join(os.getcwd(), "data", "tfidf_cache.pkl")

class NLPEngine:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.chunks = []
        self._initialize()

    def _initialize(self):
        """Load text and build/load TF-IDF index"""
        if os.path.exists(CACHE_PATH):
            try:
                with open(CACHE_PATH, 'rb') as f:
                    data = pickle.load(f)
                    self.vectorizer = data['vectorizer']
                    self.tfidf_matrix = data['matrix']
                    self.chunks = data['chunks']
                return
            except Exception:
                pass  # Fallback to rebuilding

        self._build_index()

    def _build_index(self):
        """Read file and build index"""
        if not os.path.exists(EBOOK_PATH):
            print(f"Warning: eBook file not found at {EBOOK_PATH}")
            return

        with open(EBOOK_PATH, 'r', encoding='utf-8') as f:
            text = f.read()

        # Split into chunks (paragraphs)
        # We split by double newline to get paragraphs
        raw_chunks = text.split('\n\n')
        self.chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 50]

        if not self.chunks:
            return

        # Create TF-IDF Matrix
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)

        # Save to cache
        try:
            os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
            with open(CACHE_PATH, 'wb') as f:
                pickle.dump({
                    'vectorizer': self.vectorizer,
                    'matrix': self.tfidf_matrix,
                    'chunks': self.chunks
                }, f)
        except Exception as e:
            print(f"Warning: Could not save TF-IDF cache: {e}")

    def search(self, query, top_k=1, threshold=0.1):
        """
        Search for the most relevant chunk.
        Returns the text of the best match or None if no good match found.
        """
        if not self.vectorizer or not self.chunks:
            return None

        # Transform query
        query_vec = self.vectorizer.transform([query])

        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Get top match
        best_idx = np.argmax(cosine_similarities)
        score = cosine_similarities[best_idx]

        if score >= threshold:
            return self.chunks[best_idx]
        
        return None

# Global instance
nlp_engine = NLPEngine()

def smart_search(query):
    return nlp_engine.search(query)
