"""
COVID Vaccine Tracker - Command Line Interface
A simple CLI tool to interact with the API
"""
import requests
import argparse
import sys
from typing import Optional

BASE_URL = "http://localhost:8000/api/v1"


def get_countries():
    """List all available countries"""
    response = requests.get(f"{BASE_URL}/countries")
    data = response.json()
    print(f"\n📋 Available Countries ({data['total_count']} total):\n")
    for i, country in enumerate(data['countries'], 1):
        print(f"{i:3}. {country}")


def get_country_stats(country: str):
    """Get vaccination stats for a specific country"""
    response = requests.get(f"{BASE_URL}/countries/{country}")
    
    if response.status_code == 404:
        print(f"❌ Country '{country}' not found")
        return
    
    data = response.json()
    
    print(f"\n📊 Vaccination Stats for {data['country']}")
    print("=" * 60)
    print(f"Total Vaccinations:       {data['total_vaccinations']:>20,}" if data['total_vaccinations'] else "N/A")
    print(f"People Vaccinated:        {data['people_vaccinated']:>20,}" if data['people_vaccinated'] else "N/A")
    print(f"Fully Vaccinated:         {data['people_fully_vaccinated']:>20,}" if data['people_fully_vaccinated'] else "N/A")
    print(f"Daily Vaccinations:       {data['daily_vaccinations']:>20,}" if data['daily_vaccinations'] else "N/A")
    print(f"\nVaccination Coverage:")
    print(f"  At least one dose:      {data['people_vaccinated_per_hundred']:>20.2f}%" if data['people_vaccinated_per_hundred'] else "N/A")
    print(f"  Fully vaccinated:       {data['people_fully_vaccinated_per_hundred']:>20.2f}%" if data['people_fully_vaccinated_per_hundred'] else "N/A")
    print(f"\nLatest Data: {data['date']}")
    print("=" * 60)


def get_forecast(country: str, days: int = 30):
    """Get ML forecast for a country"""
    response = requests.get(
        f"{BASE_URL}/forecast/{country}",
        params={"days": days}
    )
    
    if response.status_code == 404:
        print(f"❌ No data available for '{country}'")
        return
    
    data = response.json()
    
    print(f"\n🔮 {days}-Day Forecast for {data['country']}")
    print("=" * 60)
    print(f"{'Date':<15} {'Predicted Value':>20} {'Lower Bound':>15} {'Upper Bound':>15}")
    print("-" * 60)
    
    for forecast_point in data['forecast'][:min(10, len(data['forecast']))]:  # Show first 10
        print(
            f"{forecast_point['date']:<15} "
            f"{forecast_point['predicted_value']:>20,.0f} "
            f"{forecast_point['lower_bound']:>15,.0f} "
            f"{forecast_point['upper_bound']:>15,.0f}"
        )
    
    if len(data['forecast']) > 10:
        print(f"\n... and {len(data['forecast']) - 10} more days\n")


def chat(message: str, language: str = "en"):
    """Chat with the AI assistant"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": message, "language": language}
    )
    
    data = response.json()
    print(f"\n🤖 AI Assistant:\n")
    print(data['message'])
    print()


def compare_countries(country1: str, country2: str):
    """Compare two countries"""
    try:
        r1 = requests.get(f"{BASE_URL}/countries/{country1}")
        r2 = requests.get(f"{BASE_URL}/countries/{country2}")
        
        if r1.status_code == 404:
            print(f"❌ Country '{country1}' not found")
            return
        if r2.status_code == 404:
            print(f"❌ Country '{country2}' not found")
            return
        
        c1 = r1.json()
        c2 = r2.json()
        
        print(f"\n⚔️ Comparison: {c1['country']} vs {c2['country']}")
        print("=" * 80)
        print(f"{'Metric':<35} {c1['country']:>20} {c2['country']:>20}")
        print("-" * 80)
        
        metrics = [
            ("Total Vaccinations", "total_vaccinations", ","),
            ("Fully Vaccinated", "people_fully_vaccinated", ","),
            ("Fully Vaccinated %", "people_fully_vaccinated_per_hundred", ".2f"),
            ("Daily Vaccinations", "daily_vaccinations", ","),
        ]
        
        for label, key, fmt in metrics:
            val1 = c1.get(key)
            val2 = c2.get(key)
            val1_str = f"{val1:{fmt}}" if val1 else "N/A"
            val2_str = f"{val2:{fmt}}" if val2 else "N/A"
            
            # Add winner indicator
            if val1 and val2:
                if val1 > val2:
                    val1_str += " ⭐"
                elif val2 > val1:
                    val2_str += " ⭐"
            
            print(f"{label:<35} {val1_str:>20} {val2_str:>20}")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="COVID-19 Vaccine Tracker CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                          # List all countries
  %(prog)s stats India                   # Get India's stats
  %(prog)s forecast India --days 30      # Get 30-day forecast
  %(prog)s chat "Is the vaccine safe?"   # Ask the AI
  %(prog)s compare India USA             # Compare two countries
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    subparsers.add_parser("list", help="List all available countries")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get country statistics")
    stats_parser.add_argument("country", help="Country name")
    
    # Forecast command
    forecast_parser = subparsers.add_parser("forecast", help="Get ML forecast")
    forecast_parser.add_argument("country", help="Country name")
    forecast_parser.add_argument("--days", type=int, default=30, help="Days to forecast (default: 30)")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with AI assistant")
    chat_parser.add_argument("message", help="Your message/question")
    chat_parser.add_argument("--lang", default="en", choices=["en", "hi", "bn", "ta", "te"], help="Language")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two countries")
    compare_parser.add_argument("country1", help="First country")
    compare_parser.add_argument("country2", help="Second country")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "list":
            get_countries()
        elif args.command == "stats":
            get_country_stats(args.country)
        elif args.command == "forecast":
            get_forecast(args.country, args.days)
        elif args.command == "chat":
            chat(args.message, args.lang)
        elif args.command == "compare":
            compare_countries(args.country1, args.country2)
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server")
        print("Make sure the API is running:")
        print("  python -m uvicorn app.experimental.main:app --port 8000\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
