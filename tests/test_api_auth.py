import requests
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.auth import create_api_key

BASE_URL = "http://localhost:8001/api/v1"

def test_api_auth():
    print("Testing API Authentication...")
    
    # 1. Test without key (Should fail)
    try:
        r = requests.get(f"{BASE_URL}/countries")
        if r.status_code == 403:
            print("PASS: Request without key blocked (403)")
        else:
            print(f"FAIL: Request without key got {r.status_code}")
    except Exception as e:
        print(f"Error connecting to API: {e}")

    # 2. Test with invalid key (Should fail)
    try:
        headers = {"X-API-Key": "sk_live_invalid_key_12345"}
        r = requests.get(f"{BASE_URL}/countries", headers=headers)
        if r.status_code == 403:
            print("PASS: Request with invalid key blocked (403)")
        else:
            print(f"FAIL: Request with invalid key got {r.status_code}")
    except Exception as e:
        print(f"Error connecting to API: {e}")

    # 3. Generate a real key and test (Should pass)
    print("\nGenerating temporary test key...")
    api_key = create_api_key("Automated Test User", "test")
    
    if api_key:
        try:
            headers = {"X-API-Key": api_key}
            r = requests.get(f"{BASE_URL}/countries", headers=headers)
            if r.status_code == 200:
                print("PASS: Request with valid key succeeded (200)")
                data = r.json()
                print(f"   Received {data.get('total_count', 0)} countries")
            else:
                print(f"FAIL: Request with valid key got {r.status_code}")
                print(r.text)
        except Exception as e:
            print(f"Error connecting to API: {e}")
    else:
        print("FAIL: Could not generate test key")

if __name__ == "__main__":
    test_api_auth()
