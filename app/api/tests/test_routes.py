"""
Unit tests for API routes
Tests vaccination data, forecasting, and chatbot endpoints
"""
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import pandas as pd
from fastapi.testclient import TestClient
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app.api.main import app
from app.api.models import VaccinationStats, ChatRequest, ForecastResponse


@pytest.fixture
def client():
    """Fixture for test client"""
    return TestClient(app)


@pytest.fixture
def mock_api_key():
    """Fixture for mock API key"""
    return "test-api-key-123"


class TestHealthEndpoints:
    """Test health check and info endpoints"""
    
    def test_root_endpoint(self, client):
        """Test GET / endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "COVID-19 Vaccine Tracker API"
    
    def test_health_check(self, client):
        """Test GET /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


class TestVaccinationEndpoints:
    """Test vaccination data endpoints"""
    
    @patch('src.storage.get_all_countries')
    @patch('src.storage.get_country_latest')
    def test_get_global_stats(self, mock_get_latest, mock_get_countries, client, mock_api_key):
        """Test GET /api/v1/global endpoint"""
        # Setup mocks
        mock_get_countries.return_value = ['India', 'USA']
        
        mock_data = pd.DataFrame({
            'total_vaccinations': [2200000000],
            'people_vaccinated': [1000000000],
            'people_fully_vaccinated': [900000000]
        })
        mock_get_latest.return_value = mock_data
        
        # Make request
        response = client.get(
            "/api/v1/global",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["country"] == "Global"
        assert data["total_vaccinations"] == 4400000000  # 2 countries * 2.2B
    
    @patch('src.storage.get_all_countries')
    @patch('src.storage.get_country_latest')
    def test_get_global_stats_no_countries(self, mock_get_latest, mock_get_countries, client, mock_api_key):
        """Test GET /api/v1/global with no countries"""
        mock_get_countries.return_value = []
        
        response = client.get(
            "/api/v1/global",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_vaccinations"] == 0
    
    @patch('src.storage.get_all_countries')
    @patch('src.storage.get_country_latest')
    def test_get_top_countries(self, mock_get_latest, mock_get_countries, client, mock_api_key):
        """Test GET /api/v1/top endpoint"""
        mock_get_countries.return_value = ['India', 'USA', 'Brazil']
        
        mock_data_india = pd.DataFrame({
            'total_vaccinations': [2200000000],
            'location': ['India']
        })
        mock_data_usa = pd.DataFrame({
            'total_vaccinations': [700000000],
            'location': ['USA']
        })
        
        def mock_latest_side_effect(country):
            if country == 'India':
                return mock_data_india
            elif country == 'USA':
                return mock_data_usa
            return None
        
        mock_get_latest.side_effect = mock_latest_side_effect
        
        response = client.get(
            "/api/v1/top?limit=2",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2
    
    def test_missing_api_key(self, client):
        """Test that API key is required"""
        response = client.get("/api/v1/global")
        assert response.status_code == 403


class TestChatbotEndpoints:
    """Test chatbot endpoints"""
    
    @patch('src.chatbot.get_chatbot_response')
    def test_chat_endpoint(self, mock_chatbot, client, mock_api_key):
        """Test POST /api/v1/chat endpoint"""
        mock_chatbot.return_value = "The COVID-19 vaccine is safe and effective."
        
        request_data = {
            "message": "Is the COVID vaccine safe?",
            "language": "en"
        }
        
        response = client.post(
            "/api/v1/chat",
            json=request_data,
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "The COVID-19 vaccine is safe and effective."
        assert data["language"] == "en"
    
    @patch('src.chatbot.get_chatbot_response')
    def test_chat_with_hindi(self, mock_chatbot, client, mock_api_key):
        """Test chat endpoint with Hindi language"""
        mock_chatbot.return_value = "COVID-19 टीका सुरक्षित है।"
        
        request_data = {
            "message": "क्या COVID वैक्सीन सुरक्षित है?",
            "language": "hi"
        }
        
        response = client.post(
            "/api/v1/chat",
            json=request_data,
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "hi"
    
    @patch('src.chatbot.get_chatbot_response')
    def test_chat_empty_message(self, mock_chatbot, client, mock_api_key):
        """Test chat endpoint with empty message"""
        request_data = {
            "message": "",
            "language": "en"
        }
        
        response = client.post(
            "/api/v1/chat",
            json=request_data,
            headers={"X-API-Key": mock_api_key}
        )
        
        # Should fail validation
        assert response.status_code == 422
    
    def test_get_supported_languages(self, client, mock_api_key):
        """Test GET /api/v1/chat/languages endpoint"""
        response = client.get(
            "/api/v1/chat/languages",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "languages" in data
        assert len(data["languages"]) == 5
        language_codes = [lang["code"] for lang in data["languages"]]
        assert "en" in language_codes
        assert "hi" in language_codes


class TestForecastEndpoints:
    """Test forecasting endpoints"""
    
    @patch('src.storage.get_country_timeseries')
    @patch('src.forecast.fit_prophet_for_country')
    def test_get_forecast(self, mock_forecast, mock_timeseries, client, mock_api_key):
        """Test GET /api/v1/forecast/{country_name} endpoint"""
        # Setup mocks
        historical_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100),
            'total_vaccinations': range(100, 200)
        })
        mock_timeseries.return_value = historical_data
        
        forecast_data = pd.DataFrame({
            'ds': pd.date_range('2024-04-10', periods=30),
            'yhat': range(200, 230),
            'yhat_lower': range(190, 220),
            'yhat_upper': range(210, 240)
        })
        mock_forecast.return_value = forecast_data
        
        response = client.get(
            "/api/v1/forecast/India?days=30",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["country"] == "India"
        assert data["metric"] == "total_vaccinations"
        assert data["forecast_days"] == 30
        assert len(data["forecast"]) == 30
        assert "predicted_value" in data["forecast"][0]
    
    @patch('src.storage.get_country_timeseries')
    def test_forecast_no_data(self, mock_timeseries, client, mock_api_key):
        """Test forecast endpoint with no historical data"""
        mock_timeseries.return_value = None
        
        response = client.get(
            "/api/v1/forecast/NonExistentCountry?days=30",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 404
        assert "No historical data" in response.json()["detail"]
    
    @patch('src.storage.get_country_timeseries')
    def test_forecast_invalid_metric(self, mock_timeseries, client, mock_api_key):
        """Test forecast endpoint with invalid metric"""
        historical_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100),
            'total_vaccinations': range(100, 200)
        })
        mock_timeseries.return_value = historical_data
        
        response = client.get(
            "/api/v1/forecast/India?days=30&metric=invalid_metric",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]
    
    @patch('src.storage.get_country_timeseries')
    @patch('src.forecast.fit_prophet_for_country')
    def test_forecast_max_days(self, mock_forecast, mock_timeseries, client, mock_api_key):
        """Test forecast endpoint with max days (180)"""
        historical_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100),
            'total_vaccinations': range(100, 200)
        })
        mock_timeseries.return_value = historical_data
        
        forecast_data = pd.DataFrame({
            'ds': pd.date_range('2024-04-10', periods=180),
            'yhat': range(200, 380),
            'yhat_lower': range(190, 370),
            'yhat_upper': range(210, 390)
        })
        mock_forecast.return_value = forecast_data
        
        response = client.get(
            "/api/v1/forecast/India?days=180",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["forecast"]) == 180
    
    def test_forecast_invalid_days(self, client, mock_api_key):
        """Test forecast endpoint with invalid days parameter"""
        response = client.get(
            "/api/v1/forecast/India?days=500",  # Max is 180
            headers={"X-API-Key": mock_api_key}
        )
        
        # FastAPI should reject this
        assert response.status_code in [422, 400]


class TestErrorHandling:
    """Test error handling"""
    
    def test_not_found_endpoint(self, client, mock_api_key):
        """Test 404 error handling"""
        response = client.get(
            "/api/v1/nonexistent",
            headers={"X-API-Key": mock_api_key}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "not found" in data["detail"].lower()
    
    def test_invalid_api_key(self, client):
        """Test invalid API key"""
        response = client.get(
            "/api/v1/global",
            headers={"X-API-Key": "invalid-key-xyz"}
        )
        
        assert response.status_code == 403


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
