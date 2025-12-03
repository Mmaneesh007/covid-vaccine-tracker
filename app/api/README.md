# 🚀 Experimental FastAPI Backend

## Overview

This is an **experimental REST API** built with FastAPI that runs **independently** from the main Streamlit application. It provides programmatic access to all vaccination data, forecasting, and chatbot features.

**Status**: 🧪 Experimental - Safe to test without affecting production Streamlit app

---

## ⚡ Quick Start

### 1. Install Dependencies

```powershell
# Install FastAPI-specific dependencies
pip install -r app/experimental/requirements-api.txt
```

### 2. Start the API Server

```powershell
# Option 1: Using the startup script
.\app\experimental\start_api.ps1

# Option 2: Direct uvicorn command
uvicorn app.experimental.main:app --reload --port 8000
```

### 3. Access the API

- **API Base URL**: <http://localhost:8000>
- **Interactive Docs (Swagger)**: <http://localhost:8000/docs>
- **Alternative Docs (ReDoc)**: <http://localhost:8000/redoc>
- **Health Check**: <http://localhost:8000/health>

---

## 📡 Available Endpoints

### Health & Info

- `GET /` - API information
- `GET /health` - Health check

### Vaccination Data

- `GET /api/v1/countries` - List all countries
- `GET /api/v1/countries/{country_name}` - Get latest stats for a country
- `GET /api/v1/countries/{country_name}/timeseries` - Get historical data

### Forecasting

- `GET /api/v1/forecast/{country_name}` - Generate ML forecast (Prophet)

### AI Chatbot

- `POST /api/v1/chat` - Send message to chatbot
- `GET /api/v1/chat/languages` - Get supported languages

---

## 🧪 Testing the API

### Using curl (Command Line)

```powershell
# Get list of countries
curl http://localhost:8000/api/v1/countries

# Get India's latest stats
curl http://localhost:8000/api/v1/countries/India

# Get forecast for India (30 days)
curl http://localhost:8000/api/v1/forecast/India?days=30

# Chat with bot
curl -X POST http://localhost:8000/api/v1/chat `
  -H "Content-Type: application/json" `
  -d '{"message": "Is the vaccine safe?", "language": "en"}'
```

### Using Browser

Simply open **<http://localhost:8000/docs>** and use the interactive Swagger UI to test all endpoints with a nice interface!

### Using Python

```python
import requests

# Get countries
response = requests.get("http://localhost:8000/api/v1/countries")
countries = response.json()
print(f"Found {countries['total_count']} countries")

# Get India stats
response = requests.get("http://localhost:8000/api/v1/countries/India")
stats = response.json()
print(f"India total vaccinations: {stats['total_vaccinations']}")

# Chat
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": "What are side effects?", "language": "en"}
)
print(response.json()["message"])
```

---

## 🏗️ Architecture

```
app/experimental/
├── __init__.py           # Package initialization
├── main.py               # FastAPI application entry point
├── config.py             # Settings and configuration
├── models.py             # Pydantic schemas for validation
├── requirements-api.txt  # API-specific dependencies
├── start_api.ps1         # Startup script
├── README.md            # This file
└── routes/              # API route handlers
    ├── __init__.py
    ├── vaccination.py   # Vaccination data endpoints
    ├── forecast.py      # Forecasting endpoints
    └── chatbot.py       # Chatbot endpoints
```

### Key Design Decisions

✅ **Zero Production Impact**: Uses existing `src/` functions via imports, no code modification  
✅ **Completely Isolated**: Runs on different port (8000 vs 8501)  
✅ **Reuses Logic**: Calls same storage/chatbot/forecast functions as Streamlit  
✅ **Automatic Validation**: Pydantic models ensure type safety  
✅ **Auto-Generated Docs**: Swagger UI at `/docs` updates automatically  

---

## 🔒 Safety Features

This experimental API is **100% safe** because:

1. ✅ **No Production Code Modified**: All `src/` and `app/streamlit_app.py` files untouched
2. ✅ **Separate Port**: API runs on 8000, Streamlit on 8501
3. ✅ **Import-Only**: Only imports existing functions, doesn't rewrite them
4. ✅ **Read-Only Database Access**: Uses same storage functions that don't modify data
5. ✅ **Easy Rollback**: Just delete `app/experimental/` folder to remove

---

## 🚀 Running Both Apps Simultaneously

### Terminal 1: Streamlit (Production)

```powershell
streamlit run app/streamlit_app.py
# Runs on http://localhost:8501
```

### Terminal 2: FastAPI (Experimental)

```powershell
.\app\experimental\start_api.ps1
# Runs on http://localhost:8000
```

Both apps work independently and can run at the same time!

---

## 📊 Example API Responses

### GET /api/v1/countries/India

```json
{
  "country": "India",
  "total_vaccinations": 2200000000,
  "people_vaccinated": 1000000000,
  "people_fully_vaccinated": 900000000,
  "daily_vaccinations": 5000000,
  "total_vaccinations_per_hundred": 160.5,
  "people_vaccinated_per_hundred": 73.0,
  "people_fully_vaccinated_per_hundred": 65.7,
  "date": "2024-01-15"
}
```

### POST /api/v1/chat

**Request:**

```json
{
  "message": "Is the vaccine safe?",
  "language": "en"
}
```

**Response:**

```json
{
  "message": "Yes, COVID-19 vaccines are safe and effective. They have undergone rigorous testing...",
  "language": "en",
  "sentiment": null
}
```

---

## 🛠️ Configuration

Edit `app/experimental/config.py` to change:

- API port (default: 8000)
- CORS origins
- Rate limiting
- Cache settings

---

## 🧪 Next Steps (Future Enhancements)

Once thoroughly tested, you could:

- [ ] Add authentication (JWT tokens)
- [ ] Add rate limiting middleware
- [ ] Add Redis caching layer
- [ ] Add request logging
- [ ] Deploy separately from Streamlit
- [ ] Create OpenAPI client SDKs
- [ ] Add GraphQL endpoint

---

## 🐛 Troubleshooting

### Port already in use

```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Import errors

Make sure you're running from the project root:

```powershell
cd "C:\Users\Manish\Desktop\COVID-19 vaccine tracker"
uvicorn app.experimental.main:app --reload --port 8000
```

### Missing dependencies

```powershell
pip install -r requirements.txt
pip install -r app/experimental/requirements-api.txt
```

---

## ✅ Testing Checklist

Before considering this production-ready:

- [ ] Test all endpoints with valid data
- [ ] Test error handling (invalid country names, etc.)
- [ ] Test with multiple simultaneous requests
- [ ] Verify no slowdown to Streamlit app
- [ ] Check database isn't locked (SQLite concurrency)
- [ ] Test CORS with frontend requests
- [ ] Review auto-generated API docs

---

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Models](https://docs.pydantic.dev/)
- [Uvicorn Server](https://www.uvicorn.org/)
- [OpenAPI Specification](https://swagger.io/specification/)

---

**Questions or Issues?** This is experimental - feel free to modify anything in this folder!
