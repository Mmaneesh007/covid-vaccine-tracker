# API Usage Examples

This folder contains example scripts demonstrating how to use the COVID-19 Vaccine Tracker API.

## Files

### 1. `basic_usage.py`

Simple examples showing how to call each API endpoint.

**Run:**

```powershell
python examples/basic_usage.py
```

**Shows:**

- Get all countries
- Get country stats
- Get time series data
- Get ML forecasts
- Chat with AI
- Compare countries

---

### 2. `cli_tool.py`

Full-featured command-line interface for the API.

**Install:**

```powershell
pip install requests  # Only  dependency
```

**Usage:**

```powershell
# List all countries
python examples/cli_tool.py list

# Get India's stats
python examples/cli_tool.py stats India

# Get 30-day forecast
python examples/cli_tool.py forecast India --days 30

# Chat with AI
python examples/cli_tool.py chat "Is the vaccine safe?"

# Compare countries
python examples/cli_tool.py compare India "United States"
```

---

## Prerequisites

Make sure the API server is running:

```powershell
python -m uvicorn app.experimental.main:app --port 8000
```

Then run the examples!
