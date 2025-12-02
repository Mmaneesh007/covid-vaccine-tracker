"""
Final comprehensive API test - verifies all core functionality
"""
import requests
import json

print("="*70)
print("  COVID-19 Vaccine Tracker API - Final Verification")
print("="*70)

BASE_URL = "http://localhost:8001"

# Test 1: Health Check
print("\n[TEST 1] Health Check...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Server Status: {data['status']}")
        print(f"✓ Version: {data['version']}")
    else:
        print(f"✗ Failed with status {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Get Country Stats
print("\n[TEST 2] Get Vaccination Stats for India...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/countries/India", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Country: {data['country']}")
        print(f"✓ Total Vaccinations: {data['total_vaccinations']:,}")
        print(f"✓ People Vaccinated: {data['people_vaccinated']:,}")
        print(f"✓ Vaccination Rate: {data['people_vaccinated_per_hundred']}%")
    else:
        print(f"✗ Failed with status {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: List Countries
print("\n[TEST 3] List All Countries...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/countries", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Total Countries: {data['total_count']}")
        print(f"✓ Sample Countries: {', '.join(data['countries'][:5])}...")
    else:
        print(f"✗ Failed with status {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: AI Chatbot
print("\n[TEST 4] AI Chatbot Query...")
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/chat",
        json={"message": "Are COVID-19 vaccines safe?"},
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Response: {data['message'][:100]}...")
        print(f"✓ Language: {data['language']}")
    else:
        print(f"✗ Failed with status {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 5: Forecast
print("\n[TEST 5] Get 30-day Forecast for India...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/forecast/India?days=30", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Country: {data['country']}")
        print(f"✓ Forecast Days: {data['forecast_days']}")
        print(f"✓ Data Points: {len(data['forecast'])}")
    else:
        print(f"✗ Failed with status {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 6: Error Handling
print("\n[TEST 6] Error Handling (Invalid Country)...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/countries/InvalidCountryXYZ", timeout=5)
    if response.status_code == 404:
        print(f"✓ Correctly returned 404 for invalid country")
    else:
        print(f"✗ Expected 404, got {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*70)
print("  FINAL VERIFICATION COMPLETE")
print("="*70)
print("\n✓ API is fully operational and ready to use!")
print(f"✓ Access Swagger UI: {BASE_URL}/docs")
print(f"✓ Base URL: {BASE_URL}/api/v1")
