import sys
import os
sys.path.append(os.getcwd())
from src.storage import get_all_countries

try:
    countries = get_all_countries()
    print(f"Successfully retrieved {len(countries)} countries.")
    print(f"First 5: {countries[:5]}")
except Exception as e:
    print(f"Error: {e}")
