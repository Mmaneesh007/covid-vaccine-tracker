"""
Example: Basic API Usage
Demonstrates simple queries to the COVID Vaccine Tracker API
"""
import requests
import json

# API Base URL
BASE_URL = "http://localhost:8000/api/v1"

def main():
    print("=" * 60)
    print("COVID-19 Vaccine Tracker API - Basic Examples")
    print("=" * 60)
    
    # Example 1: Get all countries
    print("\n📊 Example 1: Get All Countries")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/countries")
    data = response.json()
    print(f"Total countries available: {data['total_count']}")
    print(f"First 10: {', '.join(data['countries'][:10])}")
    
    # Example 2: Get specific country stats
    print("\n📊 Example 2: Get India's Latest Stats")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/countries/India")
    india = response.json()
    print(f"Country: {india['country']}")
    print(f"Total Vaccinations: {india['total_vaccinations']:,}")
    print(f"Fully Vaccinated: {india['people_fully_vaccinated']:,}")
    print(f"% Fully Vaccinated: {india['people_fully_vaccinated_per_hundred']:.2f}%")
    print(f"Latest Data: {india['date']}")
    
    # Example 3: Get time series data
    print("\n📊 Example 3: Get India's Recent Vaccination Trend")
    print("-" * 60)
    response = requests.get(
        f"{BASE_URL}/countries/India/timeseries",
        params={
            "metric": "total_vaccinations",
            "limit": 7  # Last 7 days
        }
    )
    timeseries = response.json()
    print(f"Last 7 days of data for {timeseries['country']}:")
    for point in timeseries['data']:
        value_str = f"{point['value']:,}" if point['value'] else "N/A"
        print(f"  {point['date']}: {value_str}")
    
    # Example 4: Get ML forecast
    print("\n🔮 Example 4: Get 7-Day Forecast for India")
    print("-" * 60)
    response = requests.get(
        f"{BASE_URL}/forecast/India",
        params={"days": 7}
    )
    forecast = response.json()
    print(f"7-day forecast for {forecast['country']}:")
    for day in forecast['forecast'][:7]:
        print(f"  {day['date']}: {day['predicted_value']:,.0f} vaccinations")
    
    # Example 5: Chat with AI
    print("\n🤖 Example 5: Chat with AI Assistant")
    print("-" * 60)
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "Is the COVID vaccine safe?",
            "language": "en"
        }
    )
    chat_response = response.json()
    print(f"Q: Is the COVID vaccine safe?")
    print(f"A: {chat_response['message'][:200]}...")  # First 200 chars
    
    # Example 6: Compare two countries
    print("\n⚔️ Example 6: Compare India vs United States")
    print("-" * 60)
    india = requests.get(f"{BASE_URL}/countries/India").json()
    usa = requests.get(f"{BASE_URL}/countries/United States").json()
    
    print(f"{'Metric':<30} {'India':>15} {'USA':>15}")
    print("-" * 60)
    print(f"{'Total Vaccinations':<30} {india['total_vaccinations']:>15,} {usa['total_vaccinations']:>15,}")
    print(f"{'Fully Vaccinated %':<30} {india['people_fully_vaccinated_per_hundred']:>15.2f} {usa['people_fully_vaccinated_per_hundred']:>15.2f}")
    
    print("\n" + "=" * 60)
    print("✅ All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API")
        print("Make sure the API server is running:")
        print("  python -m uvicorn app.experimental.main:app --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")
