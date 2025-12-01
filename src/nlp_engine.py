import os
import pickle
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Path to knowledge sources
KNOWLEDGE_FOLDER = os.path.join(os.getcwd(), "knowledge")
LEGACY_EBOOK_PATH = os.path.join(os.getcwd(), "extracted_ebook_text.txt")
CACHE_PATH = os.path.join(os.getcwd(), "data", "tfidf_cache.pkl")

class NLPEngine:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.chunks = []
        self.sources = []  # Track which source each chunk came from
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
                    self.sources = data.get('sources', [])
                print(f"Loaded TF-IDF cache with {len(self.chunks)} chunks from {len(set(self.sources))} sources")
                return
            except Exception as e:
                print(f"Cache load failed: {e}, rebuilding...")

        self._build_index()

    def _build_index(self):
        """Read all files and build index"""
        all_text = []
        
        # Create knowledge folder if it doesn't exist
        os.makedirs(KNOWLEDGE_FOLDER, exist_ok=True)
        
        # Find all .txt files in knowledge folder
        knowledge_files = glob.glob(os.path.join(KNOWLEDGE_FOLDER, "*.txt"))
        
        # Also check for legacy ebook file
        if os.path.exists(LEGACY_EBOOK_PATH):
            knowledge_files.append(LEGACY_EBOOK_PATH)
        
        if not knowledge_files:
            print(f"Warning: No knowledge sources found in {KNOWLEDGE_FOLDER}")
            return
        
        print(f"Loading knowledge from {len(knowledge_files)} file(s):")
        
        # Read and combine all files
        for filepath in knowledge_files:
            try:
                filename = os.path.basename(filepath)
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                # Split into paragraphs
                raw_chunks = text.split('\n\n')
                file_chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 50]
                
                all_text.extend(file_chunks)
                self.sources.extend([filename] * len(file_chunks))
                
                print(f"  [OK] {filename}: {len(file_chunks)} paragraphs")
            except Exception as e:
                print(f"  [FAIL] Failed to load {filepath}: {e}")
        
        self.chunks = all_text
        
        if not self.chunks:
            return

        # Create TF-IDF Matrix
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)

        # Save to cache
        try:
            os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
            with open(CACHE_PATH, 'wb') as f:
                pickle.dump({
                    'vectorizer': self.vectorizer,
                    'matrix': self.tfidf_matrix,
                    'chunks': self.chunks,
                    'sources': self.sources
                }, f)
            print(f"Saved TF-IDF cache with {len(self.chunks)} total chunks")
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
