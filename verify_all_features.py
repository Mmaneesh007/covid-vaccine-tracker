import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

def verify_imports():
    print("Verifying imports for new features...")
    
    # 1. Simulator
    try:
        from src.simulation import render_simulator
        print("[OK] Simulator module imported")
    except ImportError as e:
        print(f"[FAIL] Simulator import failed: {e}")
        return False

    # 2. Voice Input
    try:
        from src.voice_input import get_voice_input
        print("[OK] Voice Input module imported")
    except ImportError as e:
        print(f"[FAIL] Voice Input import failed: {e}")
        return False

    # 3. NLP Engine
    try:
        from src.nlp_engine import smart_search
        print("[OK] NLP Engine module imported")
    except ImportError as e:
        print(f"[FAIL] NLP Engine import failed: {e}")
        return False

    # 4. Comparison
    try:
        from src.comparison import render_comparison
        print("[OK] Comparison module imported")
    except ImportError as e:
        print(f"[FAIL] Comparison import failed: {e}")
        return False
        
    print("\nAll new features verified successfully!")
    return True

if __name__ == "__main__":
    if verify_imports():
        sys.exit(0)
    else:
        sys.exit(1)
