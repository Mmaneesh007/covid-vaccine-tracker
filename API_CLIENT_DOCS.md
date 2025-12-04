# COVID-19 Vaccine Tracker API - Client Documentation

**Version**: 1.0  
**Base URL**: `http://localhost:8001/api/v1`  
**Authentication**: API Key (Header-based)

---

## 🚀 Quick Start

### 1. Get Your API Key

Contact the API administrator to receive your unique API key. It will look like:

```
YOUR_API_KEY_HERE
```

⚠️ **Keep your API key secure!** Never commit it to version control or share it publicly.

### 2. Make Your First Request

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "http://localhost:8001/api/v1"

headers = {"X-API-Key": API_KEY}
response = requests.get(f"{BASE_URL}/countries", headers=headers)

print(response.json())
```

---

## 🔐 Authentication

All API requests require an `X-API-Key` header:

```http
GET /api/v1/countries HTTP/1.1
Host: localhost:8001
X-API-Key: your_api_key_here
```

### Authentication Errors

| Status Code | Meaning |
|-------------|---------|
| `403` | Missing or invalid API key |
| `200` | Success |

---

## 📡 Endpoints

### 1. List All Countries

Get a list of all countries with vaccination data.

**Endpoint**: `GET /countries`

**Response**:

```json
{
  "countries": ["Afghanistan", "Albania", "Algeria", ...],
  "total_count": 255
}
```

**Example**:

```python
response = requests.get(f"{BASE_URL}/countries", headers=headers)
countries = response.json()['countries']
```

---

### 2. Get Country Statistics

Get the latest vaccination statistics for a specific country.

**Endpoint**: `GET /countries/{country_name}`

**Parameters**:

- `country_name` (path): Country name (e.g., "India", "United States")

**Response**:

```json
{
  "location": "India",
  "date": "2024-01-15",
  "total_vaccinations": 2206868000,
  "people_vaccinated": 1043210000,
  "people_fully_vaccinated": 982145000,
  "pct_vaccinated": 75.8,
  "daily_vaccinations": 125000
}
```

**Example**:

```python
response = requests.get(f"{BASE_URL}/countries/India", headers=headers)
india_data = response.json()
print(f"Total doses: {india_data['total_vaccinations']:,}")
```

---

### 3. Get Time Series Data

Get historical vaccination data for a country.

**Endpoint**: `GET /countries/{country_name}/timeseries`

**Response**:

```json
{
  "location": "India",
  "data": [
    {
      "date": "2021-01-16",
      "total_vaccinations": 191181,
      "daily_vaccinations": 16757
    },
    ...
  ]
}
```

**Example**:

```python
response = requests.get(f"{BASE_URL}/countries/India/timeseries", headers=headers)
time_series = response.json()['data']
```

---

### 4. Generate Forecast

Get ML-based vaccination forecast for a country.

**Endpoint**: `GET /forecast/{country_name}?days=30`

**Parameters**:

- `country_name` (path): Country name
- `days` (query, optional): Number of days to forecast (default: 30)

**Response**:

```json
{
  "country": "India",
  "forecast_days": 30,
  "forecast": [
    {
      "ds": "2024-02-15",
      "yhat": 125000,
      "yhat_lower": 100000,
      "yhat_upper": 150000
    },
    ...
  ]
}
```

**Example**:

```python
response = requests.get(f"{BASE_URL}/forecast/India?days=30", headers=headers)
forecast = response.json()['forecast']
```

---

### 5. Chat with AI Assistant

Send a message to the AI Health Assistant.

**Endpoint**: `POST /chat`

**Request Body**:

```json
{
  "message": "Is the COVID vaccine safe?",
  "language": "en"
}
```

**Supported Languages**: `en`, `hi`, `bn`, `ta`, `te`

**Response**:

```json
{
  "message": "Yes, COVID-19 vaccines are safe and effective...",
  "language": "en"
}
```

**Example**:

```python
payload = {
    "message": "What are the side effects?",
    "language": "en"
}
response = requests.post(f"{BASE_URL}/chat", json=payload, headers=headers)
answer = response.json()['message']
```

---

## 💻 Code Examples

### Python

```python
import requests

class VaccineTrackerAPI:
    def __init__(self, api_key):
        self.base_url = "http://localhost:8001/api/v1"
        self.headers = {"X-API-Key": api_key}
    
    def get_countries(self):
        response = requests.get(f"{self.base_url}/countries", headers=self.headers)
        return response.json()
    
    def get_country_stats(self, country):
        response = requests.get(f"{self.base_url}/countries/{country}", headers=self.headers)
        return response.json()
    
    def get_forecast(self, country, days=30):
        response = requests.get(
            f"{self.base_url}/forecast/{country}",
            params={"days": days},
            headers=self.headers
        )
        return response.json()

# Usage
api = VaccineTrackerAPI("your_api_key_here")
stats = api.get_country_stats("India")
print(stats)
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const API_KEY = 'your_api_key_here';
const BASE_URL = 'http://localhost:8001/api/v1';

const headers = { 'X-API-Key': API_KEY };

// Get countries
axios.get(`${BASE_URL}/countries`, { headers })
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error('Error:', error.response.data);
  });

// Get country stats
axios.get(`${BASE_URL}/countries/India`, { headers })
  .then(response => {
    console.log(response.data);
  });
```

### cURL

```bash
# Get countries
curl -X GET "http://localhost:8001/api/v1/countries" \
  -H "X-API-Key: your_api_key_here"

# Get India stats
curl -X GET "http://localhost:8001/api/v1/countries/India" \
  -H "X-API-Key: your_api_key_here"

# Chat with AI
curl -X POST "http://localhost:8001/api/v1/chat" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"message": "Is the vaccine safe?", "language": "en"}'
```

---

## ⚠️ Error Handling

Always handle API errors gracefully:

```python
try:
    response = requests.get(f"{BASE_URL}/countries/India", headers=headers)
    response.raise_for_status()  # Raises HTTPError for bad responses
    data = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 403:
        print("Invalid API key")
    elif e.response.status_code == 404:
        print("Country not found")
    else:
        print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## 📊 Rate Limits

**Current Tier**: Free  
**Limit**: 100 requests per day  
**Reset**: Daily at 00:00 UTC

Response headers include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1704153600
```

---

## 🔧 Best Practices

### 1. Store API Keys Securely

**❌ Don't:**

```python
API_KEY = "sk_live_XXXXXXXX"  # Hardcoded - DON'T DO THIS!
```

**✅ Do:**

```python
import os
API_KEY = os.getenv("VACCINE_API_KEY")  # Environment variable
```

### 2. Handle Timeouts

```python
response = requests.get(url, headers=headers, timeout=10)
```

### 3. Retry Failed Requests

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
```

### 4. Cache Responses

```python
import requests_cache

requests_cache.install_cache('vaccine_cache', expire_after=3600)
```

---

## 📚 Interactive Documentation

Visit the **Swagger UI** for interactive API testing:

👉 **<http://localhost:8001/docs>**

Features:

- Try endpoints directly in the browser
- See request/response schemas
- Generate code snippets

---

## 🆘 Support

**Issues**: Report bugs or request features on GitHub  
**Email**: <support@example.com>  
**Docs**: Full documentation at `/docs`

---

## 📄 License & Terms

- API access provided under MIT License
- Data sourced from [Our World in Data](https://ourworldindata.org/)
- Usage subject to fair use policy
- Commercial use allowed with attribution

---

**Last Updated**: December 2024  
**API Version**: 1.0
