import argparse
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def check_connection():
    try:
        requests.get("http://localhost:8000/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API at http://localhost:8000")
        print("   Please ensure the API server is running: .\\app\\experimental\\start_api.ps1")
        sys.exit(1)

def handle_list_countries(args):
    response = requests.get(f"{BASE_URL}/countries")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total_count']} countries:")
        for country in data['countries']:
            print(f"  - {country}")
    else:
        print(f"❌ Error: {response.text}")

def handle_stats(args):
    response = requests.get(f"{BASE_URL}/countries/{args.country}")
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Stats for {data['country']} ({data['date']})")
        print("-" * 40)
        print(f"Total Vaccinations:      {data['total_vaccinations']:,}")
        print(f"People Vaccinated:       {data['people_vaccinated']:,}")
        print(f"People Fully Vaccinated: {data['people_fully_vaccinated']:,}")
        print(f"Daily Vaccinations:      {data['daily_vaccinations']:,}")
        print("-" * 40)
    else:
        print(f"❌ Error: {response.text}")

def handle_forecast(args):
    response = requests.get(f"{BASE_URL}/forecast/{args.country}?days={args.days}")
    if response.status_code == 200:
        data = response.json()
        print(f"\n🔮 Forecast for {args.country} (Next {args.days} days)")
        print("-" * 60)
        print(f"{'Date':<12} | {'Forecast':<15} | {'Trend':<15}")
        print("-" * 60)
        for day in data['forecast']:
            print(f"{day['ds']:<12} | {day['yhat']:<15.0f} | {day['trend']:<15.0f}")
    else:
        print(f"❌ Error: {response.text}")

def handle_chat(args):
    payload = {"message": args.message, "language": args.lang}
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"\n🤖 AI Response ({data['language']}):")
        print(f"\"{data['message']}\"")
    else:
        print(f"❌ Error: {response.text}")

def main():
    parser = argparse.ArgumentParser(description="COVID-19 Vaccine Tracker API CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List Countries
    subparsers.add_parser("list-countries", help="List all available countries")

    # Country Stats
    stats_parser = subparsers.add_parser("stats", help="Get vaccination stats for a country")
    stats_parser.add_argument("--country", "-c", required=True, help="Country name")

    # Forecast
    forecast_parser = subparsers.add_parser("forecast", help="Get vaccination forecast")
    forecast_parser.add_argument("--country", "-c", required=True, help="Country name")
    forecast_parser.add_argument("--days", "-d", type=int, default=7, help="Number of days to forecast")

    # Chat
    chat_parser = subparsers.add_parser("chat", help="Chat with the AI assistant")
    chat_parser.add_argument("--message", "-m", required=True, help="Message to send")
    chat_parser.add_argument("--lang", "-l", default="en", help="Language code (en, hi, bn, ta, te)")

    args = parser.parse_args()

    if args.command:
        check_connection()
        if args.command == "list-countries":
            handle_list_countries(args)
        elif args.command == "stats":
            handle_stats(args)
        elif args.command == "forecast":
            handle_forecast(args)
        elif args.command == "chat":
            handle_chat(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
