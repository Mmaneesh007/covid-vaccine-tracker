# API Usage Examples

This folder contains example scripts demonstrating how to use the COVID-19 Vaccine Tracker API.

## Files

### 1. `basic_queries.py` & `basic_usage.py`

Simple scripts demonstrating how to fetch data, get stats, and chat with the bot.

### 2. `api_cli.py` & `cli_tool.py`

Command-line tools for interacting with the API.

```powershell
python examples/api_cli.py stats --country "India"
```

### 3. `analysis_notebook.py`

A data analysis script (VS Code notebook format) that compares vaccination rates and plots forecasts.

### 4. `USE_CASES.md`

Documentation describing common scenarios like building mobile apps or automated reports.

---

## Prerequisites

Make sure the API server is running:

```powershell
python -m uvicorn app.experimental.main:app --port 8000
```

Then run the examples!
