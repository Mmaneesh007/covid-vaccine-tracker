# COVID-19 Vaccine Tracker SDK

Official Python SDK for the **COVID-19 Vaccine Tracker API**.

[![PyPI version](https://badge.fury.io/py/vaccine-tracker-sdk.svg)](https://badge.fury.io/py/vaccine-tracker-sdk)
[![Python](https://img.shields.io/pypi/pyversions/vaccine-tracker-sdk.svg)](https://pypi.org/project/vaccine-tracker-sdk/)

## 📦 Installation

```bash
pip install vaccine-tracker-sdk
```

Or install from source:

```bash
git clone https://github.com/Mmaneesh007/covid-vaccine-tracker.git
cd covid-vaccine-tracker/sdk
pip install -e .
```

## 🚀 Quick Start

```python
from vaccine_tracker_sdk import VaccineTrackerAPI

# Initialize the client
api = VaccineTrackerAPI(api_key="sk_live_your_api_key_here")

# Get all countries
countries = api.get_countries()
print(f"Total countries: {len(countries)}")

# Get India's stats
india = api.get_country("India")
print(f"India - Total doses: {india['total_vaccinations']:,}")

# Get 30-day forecast
forecast = api.get_forecast("India", days=30)
print(f"Forecast generated for {len(forecast['forecast'])} days")

# Chat with AI
response = api.chat("Is the vaccine safe?")
print(response)
```

## 📖 Documentation

### Initialize Client

```python
from vaccine_tracker_sdk import VaccineTrackerAPI

api = VaccineTrackerAPI(
    api_key="your_api_key",
    base_url="http://localhost:8001/api/v1"  # Optional
)
```

### Get Countries

```python
countries = api.get_countries()
# Returns: ['Afghanistan', 'Albania', ...]
```

### Get Country Statistics

```python
stats = api.get_country("India")
# Returns: {
#   'location': 'India',
#   'total_vaccinations': 2206868000,
#   'pct_vaccinated': 75.8,
#   ...
# }
```

### Get Time Series

```python
data = api.get_country_timeseries("India")
# Returns historical data for India
```

### Generate Forecast

```python
forecast = api.get_forecast("India", days=30)
# Returns ML-based 30-day forecast
```

### Chat with AI

```python
answer = api.chat("What are the side effects?", language="en")
# Supported languages: en, hi, bn, ta, te
```

### Compare Countries

```python
comparison = api.compare_countries("India", "United States")
print(comparison['comparison'])
# Shows difference in vaccination rates
```

### Search Countries

```python
results = api.search_countries("united")
# Returns: ['United Kingdom', 'United States', ...]
```

## 🔑 Getting an API Key

Contact the API administrator or visit the Admin Portal to generate your API key.

## ⚠️ Error Handling

```python
from vaccine_tracker_sdk import VaccineTrackerAPI

api = VaccineTrackerAPI(api_key="your_key")

try:
    stats = api.get_country("InvalidCountry")
except ValueError as e:
    print(f"Error: {e}")  # "Resource not found"
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🌐 Environment Variables

Store your API key securely:

```bash
export VACCINE_API_KEY="sk_live_your_key"
```

```python
import os
from vaccine_tracker_sdk import VaccineTrackerAPI

api = VaccineTrackerAPI(api_key=os.getenv("VACCINE_API_KEY"))
```

## 🧪 Development

Install dev dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest tests/
```

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Mmaneesh007/covid-vaccine-tracker/issues)
- **Docs**: [Full API Documentation](https://github.com/Mmaneesh007/covid-vaccine-tracker/blob/main/API_CLIENT_DOCS.md)

## 🙏 Credits

Data provided by [Our World in Data](https://ourworldindata.org/)
