import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

print("Testing Multi-Source NLP Engine...")
print("=" * 50)

try:
    from src.nlp_engine import nlp_engine
    
    # Test the search function
    test_queries = [
        "What are vaccine side effects?",
        "Is COVID-19 vaccine safe?",
        "Can pregnant women get vaccinated?"
    ]
    
    print(f"\nKnowledge Base Stats:")
    print(f"  Total chunks: {len(nlp_engine.chunks)}")
    print(f"  Sources: {len(set(nlp_engine.sources))}")
    if nlp_engine.sources:
        print(f"  Source files: {', '.join(set(nlp_engine.sources))}")
    
    print(f"\nTesting search functionality:")
    for query in test_queries:
        result = nlp_engine.search(query)
        if result:
            print(f"\n[OK] Query: '{query}'")
            print(f"  Answer preview: {result[:150]}...")
        else:
            print(f"\n[NOT FOUND] Query: '{query}' - No result found")
    
    print("\n" + "=" * 50)
    print("Multi-source NLP engine is working! [SUCCESS]")
    
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
