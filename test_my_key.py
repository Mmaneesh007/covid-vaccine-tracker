"""
Quick test script for the API key.
"""
import requests

API_KEY = "sk_live_e7d7160fe461379b6e42050c99e62dec"
BASE_URL = "http://localhost:8001/api/v1"

def test_api_key():
    print("=" * 50)
    print("Testing API Key Authentication")
    print("=" * 50)
    
    headers = {"X-API-Key": API_KEY}
    
    # Test 1: Get all countries
    print("\n[TEST 1] Fetching countries list...")
    try:
        response = requests.get(f"{BASE_URL}/countries", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Received {data.get('total_count', 0)} countries")
            print(f"Sample countries: {data.get('countries', [])[:5]}")
        else:
            print(f"FAILED: Status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Test 2: Get specific country stats
    print("\n[TEST 2] Fetching India's vaccination stats...")
    try:
        response = requests.get(f"{BASE_URL}/countries/India", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: India Data Retrieved")
            print(f"  Location: {data.get('location')}")
            print(f"  Total Vaccinations: {data.get('total_vaccinations'):,}")
            print(f"  Coverage: {data.get('pct_vaccinated'):.2f}%")
        else:
            print(f"FAILED: Status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Test 3: Test without key (should fail)
    print("\n[TEST 3] Testing security (no key)...")
    try:
        response = requests.get(f"{BASE_URL}/countries")
        if response.status_code == 403:
            print("SUCCESS: Unauthorized request blocked (403)")
        else:
            print(f"SECURITY ISSUE: Got status {response.status_code} instead of 403")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("All tests complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_api_key()
