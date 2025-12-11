"""
Comprehensive Test Suite for FastAPI Experimental Backend
Tests all endpoints: Health, Vaccination Data, Forecasting, and AI Chatbot
"""
import requests
import json
from datetime import datetime
from src.auth import create_api_key

# API Configuration
BASE_URL = "http://localhost:8001"
API_PREFIX = "/api/v1"

# Generate API key for authenticated endpoints
API_KEY = create_api_key("API Test Suite", "test")
DEFAULT_HEADERS = {"X-API-Key": API_KEY} if API_KEY else {}

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def test_endpoint(method, endpoint, description, data=None, expected_status=200, headers=DEFAULT_HEADERS):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n[TEST] Testing: {description}")
    print(f"   Endpoint: {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"   [PASS] SUCCESS")
            try:
                result = response.json()
                print(f"   Response Preview: {json.dumps(result, indent=2)[:200]}...")
                return True
            except:
                print(f"   Response: {response.text[:200]}...")
                return True
        else:
            print(f"   [FAIL] FAILED - Expected {expected_status}, got {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   [FAIL] FAILED - Connection Error: Is the API server running?")
        return False
    except requests.exceptions.Timeout:
        print(f"   [FAIL] FAILED - Request Timeout")
        return False
    except Exception as e:
        print(f"   [FAIL] FAILED - {str(e)}")
        return False

def main():
    """Run all API tests"""
    print("\n" + "="*70)
    print("   COVID-19 Vaccine Tracker API - Test Suite")
    print("="*70)
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    # =============================================================================
    # TEST 1: Health Endpoints
    # =============================================================================
    print_section("TEST 1: HEALTH ENDPOINTS")
    
    # Test root endpoint
    if test_endpoint("GET", "/", "Root endpoint - API information"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test health check
    if test_endpoint("GET", "/health", "Health check endpoint"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # =============================================================================
    # TEST 2: Vaccination Data Endpoints
    # =============================================================================
    print_section("TEST 2: VACCINATION DATA ENDPOINTS")
    
    # Test get all countries
    if test_endpoint("GET", f"{API_PREFIX}/countries", "Get list of all countries"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test vaccination stats for India
    if test_endpoint("GET", f"{API_PREFIX}/countries/India", "Get vaccination stats for India"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test vaccination stats for United States
    if test_endpoint("GET", f"{API_PREFIX}/countries/United States", "Get vaccination stats for United States"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test time series data for India
    if test_endpoint("GET", f"{API_PREFIX}/countries/India/timeseries", "Get time series data for India"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test global stats
    if test_endpoint("GET", f"{API_PREFIX}/global", "Get global vaccination statistics"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test top performers
    if test_endpoint("GET", f"{API_PREFIX}/top?limit=10", "Get top 10 performing countries"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # =============================================================================
    # TEST 3: Forecasting Endpoints
    # =============================================================================
    print_section("TEST 3: FORECASTING ENDPOINTS")
    
    # Test forecast for India
    if test_endpoint("GET", f"{API_PREFIX}/forecast/India?days=30", "Get 30-day forecast for India"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test forecast for United States
    if test_endpoint("GET", f"{API_PREFIX}/forecast/United States?days=60", "Get 60-day forecast for United States"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # =============================================================================
    # TEST 4: AI Chatbot Endpoint
    # =============================================================================
    print_section("TEST 4: AI CHATBOT ENDPOINTS")
    
    # Test chatbot with vaccine safety question
    chatbot_data_1 = {
        "message": "Are COVID-19 vaccines safe?"
    }
    if test_endpoint("POST", f"{API_PREFIX}/chat", "Ask about vaccine safety", data=chatbot_data_1):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test chatbot with side effects question
    chatbot_data_2 = {
        "message": "What are common vaccine side effects?"
    }
    if test_endpoint("POST", f"{API_PREFIX}/chat", "Ask about side effects", data=chatbot_data_2):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test chatbot with vaccination data question
    chatbot_data_3 = {
        "message": "How many people are vaccinated in India?"
    }
    if test_endpoint("POST", f"{API_PREFIX}/chat", "Ask about India vaccination stats", data=chatbot_data_3):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # =============================================================================
    # TEST 5: Error Handling
    # =============================================================================
    print_section("TEST 5: ERROR HANDLING")
    
    # Test invalid country
    if test_endpoint("GET", f"{API_PREFIX}/countries/InvalidCountry123", 
                     "Test invalid country (should return 404)", expected_status=404):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test invalid endpoint
    if test_endpoint("GET", f"{API_PREFIX}/invalid/endpoint", 
                     "Test non-existent endpoint (should return 404)", expected_status=404):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # =============================================================================
    # SUMMARY
    # =============================================================================
    print_section("TEST SUMMARY")
    print(f"\n   Total Tests: {results['total']}")
    print(f"   [PASS] Passed: {results['passed']}")
    print(f"   [FAIL] Failed: {results['failed']}")
    print(f"   Success Rate: {(results['passed']/results['total']*100):.1f}%\n")
    
    if results['failed'] == 0:
        print("   *** ALL TESTS PASSED! ***\n")
    else:
        print(f"   WARNING: {results['failed']} test(s) failed. Please review the output above.\n")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
