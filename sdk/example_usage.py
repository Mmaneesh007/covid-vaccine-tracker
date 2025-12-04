"""
Example usage of the COVID-19 Vaccine Tracker SDK
"""
import os
from vaccine_tracker_sdk import VaccineTrackerAPI

# Get API key from environment variable (recommended)
API_KEY = os.getenv("VACCINE_API_KEY", "sk_live_your_api_key_here")

def main():
    # Initialize the API client
    print("Initializing COVID-19 Vaccine Tracker SDK...")
    api = VaccineTrackerAPI(api_key=API_KEY)
    
    # Example 1: Get all countries
    print("\n=== Example 1: Get All Countries ===")
    countries = api.get_countries()
    print(f"Total countries available: {len(countries)}")
    print(f"First 10 countries: {countries[:10]}")
    
    # Example 2: Get specific country stats
    print("\n=== Example 2: Get India Statistics ===")
    india = api.get_country("India")
    print(f"Location: {india.get('location')}")
    print(f"Total Vaccinations: {india.get('total_vaccinations', 0):,}")
    print(f"Population Coverage: {india.get('pct_vaccinated', 0):.2f}%")
    
    # Example 3: Compare two countries
    print("\n=== Example 3: Compare Countries ===")
    comparison = api.compare_countries("India", "United States")
    diff = comparison['comparison']['vaccination_rate_difference']
    print(f"Vaccination rate difference: {diff:.2f}%")
    
    # Example 4: Get forecast
    print("\n=== Example 4: Get 30-Day Forecast ===")
    forecast = api.get_forecast("India", days=30)
    print(f"Forecast generated for: {forecast['country']}")
    print(f"Number of forecast days: {forecast['forecast_days']}")
    first_forecast = forecast['forecast'][0]
    print(f"First day prediction: {first_forecast['yhat']:.0f} doses")
    
    # Example 5: Chat with AI
    print("\n=== Example 5: Ask AI Health Assistant ===")
    questions = [
        "Is the COVID vaccine safe?",
        "What are common side effects?",
        "How effective is the vaccine?"
    ]
    
    for question in questions:
        answer = api.chat(question)
        print(f"\nQ: {question}")
        print(f"A: {answer[:200]}...")  # First 200 chars
    
    # Example 6: Search countries
    print("\n=== Example 6: Search Countries ===")
    results = api.search_countries("United")
    print(f"Countries matching 'United': {results}")
    
    # Example 7: Get time series
    print("\n=== Example 7: Get Historical Data ===")
    timeseries = api.get_country_timeseries("India")
    data_points = timeseries.get('data', [])
    print(f"Total historical data points: {len(data_points)}")
    if data_points:
        latest = data_points[-1]
        print(f"Latest date: {latest.get('date')}")
        print(f"Total vaccinations on that date: {latest.get('total_vaccinations', 0):,}")
    
    print("\n=== All Examples Complete! ===")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"\n❌ Authentication Error: {e}")
        print("Make sure you have a valid API key set in the VACCINE_API_KEY environment variable")
    except Exception as e:
        print(f"\n❌ Error: {e}")
