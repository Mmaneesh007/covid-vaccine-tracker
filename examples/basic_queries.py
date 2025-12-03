import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}\n")

def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get(f"http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ API is online and healthy!")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Is it running?")
        print("   Run: .\\app\\experimental\\start_api.ps1")
        return False

def get_countries():
    """Fetch and list available countries."""
    print_section("1. Fetching Countries")
    response = requests.get(f"{BASE_URL}/countries")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} countries.")
        print(f"First 5: {data['countries'][:5]}")
    else:
        print("Error fetching countries")

def get_country_stats(country):
    """Get statistics for a specific country."""
    print_section(f"2. Stats for {country}")
    response = requests.get(f"{BASE_URL}/countries/{country}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error fetching stats for {country}")

def get_forecast(country):
    """Get vaccination forecast."""
    print_section(f"3. Forecast for {country}")
    response = requests.get(f"{BASE_URL}/forecast/{country}?days=7")
    if response.status_code == 200:
        data = response.json()
        forecast = data['forecast']
        print(f"Forecast for next 7 days:")
        for day in forecast:
            print(f"  {day['ds']}: {day['yhat']:.0f} doses (Trend: {day['trend']:.0f})")
    else:
        print(f"Error fetching forecast for {country}")

def chat_with_bot(message):
    """Send a message to the AI chatbot."""
    print_section(f"4. Chatbot Query: '{message}'")
    payload = {
        "message": message,
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"🤖 Bot: {data['message']}")
    else:
        print("Error communicating with chatbot")

def main():
    if not check_api_health():
        return

    get_countries()
    get_country_stats("India")
    get_forecast("USA")
    chat_with_bot("Is the vaccine safe for children?")

if __name__ == "__main__":
    main()
