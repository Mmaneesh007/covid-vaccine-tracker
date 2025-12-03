import pandas as pd
from datetime import datetime, timedelta
from src.insights import generate_country_insight, generate_global_insight

def test_insights():
    print("Testing AI Insights Generation...")
    
    # Create mock data
    df = pd.DataFrame({
        'location': ['India', 'India', 'USA', 'USA'],
        'date': [
            datetime.now() - timedelta(days=7),
            datetime.now(),
            datetime.now() - timedelta(days=7),
            datetime.now()
        ],
        'daily_vaccinations_7d': [1_200_000, 1_380_000, 500_000, 550_000],
        'pct_vaccinated': [65.5, 67.2, 72.1, 73.5],
        'total_vaccinations': [1.2e9, 1.3e9, 500e6, 520e6],
        'people_vaccinated': [800e6, 820e6, 350e6, 360e6],
        'population': [1.4e9, 1.4e9, 330e6, 330e6]
    })
    
    print("\n=== Testing Country Insight ===")
    try:
        india_insight = generate_country_insight(df, 'India')
        print(f"[OK] India: {india_insight}")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
    
    print("\n=== Testing Global Insight ===")
    try:
        global_insight = generate_global_insight(df)
        print(f"[OK] Global: {global_insight}")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
    
    print("\n[SUCCESS] All tests completed!")

if __name__ == "__main__":
    test_insights()
