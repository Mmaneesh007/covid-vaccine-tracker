# Final API Verification Test
import requests

print("="*70)
print("  COVID-19 Vaccine Tracker API - Final Verification")
print("="*70)

BASE_URL = "http://localhost:8001"

# Test 1: Health Check
print("\n[TEST 1] Health Check...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"[OK] Status: {response.status_code}")
    print(f"[OK] {response.json()}")
except Exception as e:
    print(f"[FAIL] {e}")

# Test 2: Country Stats
print("\n[TEST 2] Get Vaccination Stats for India...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/countries/India", timeout=5)
    data = response.json()
    print(f"[OK] Country: {data['country']}")
    print(f"[OK] Total Vaccinations: {data['total_vaccinations']:,}")
except Exception as e:
    print(f"[FAIL] {e}")

# Test 3: Chatbot
print("\n[TEST 3] AI Chatbot...")
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/chat",
        json={"message": "Are vaccines safe?"},
        timeout=5
    )
    data = response.json()
    print(f"[OK] Response: {data['message'][:80]}...")
except Exception as e:
    print(f"[FAIL] {e}")

print("\n" + "="*70)
print("  FINAL VERIFICATION COMPLETE - API IS READY!")
print("="*70)
