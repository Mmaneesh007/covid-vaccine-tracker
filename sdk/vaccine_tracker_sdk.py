"""
COVID-19 Vaccine Tracker API - Python SDK
Official Python client for the COVID-19 Vaccine Tracker API.
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime


class VaccineTrackerAPI:
    """
    Official Python SDK for the COVID-19 Vaccine Tracker API.
    
    Example:
        >>> from vaccine_tracker_sdk import VaccineTrackerAPI
        >>> api = VaccineTrackerAPI(api_key="sk_live_...")
        >>> countries = api.get_countries()
        >>> india = api.get_country("India")
    """
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8001/api/v1"):
        """
        Initialize the API client.
        
        Args:
            api_key: Your API key (get from the admin portal)
            base_url: API base URL (default: localhost:8001)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {"X-API-Key": api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make an HTTP request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise ValueError("Invalid API key. Check your credentials.")
            elif e.response.status_code == 404:
                raise ValueError(f"Resource not found: {endpoint}")
            else:
                raise Exception(f"API error ({e.response.status_code}): {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
    
    # ==================== Country Endpoints ====================
    
    def get_countries(self) -> List[str]:
        """
        Get a list of all available countries.
        
        Returns:
            List of country names
            
        Example:
            >>> countries = api.get_countries()
            >>> print(countries[:5])
            ['Afghanistan', 'Albania', 'Algeria', ...]
        """
        response = self._request("GET", "/countries")
        return response.get("countries", [])
    
    def get_country(self, country_name: str) -> Dict:
        """
        Get the latest vaccination statistics for a specific country.
        
        Args:
            country_name: Name of the country (e.g., "India", "United States")
            
        Returns:
            Dictionary with vaccination statistics
            
        Example:
            >>> india = api.get_country("India")
            >>> print(f"Total doses: {india['total_vaccinations']:,}")
        """
        return self._request("GET", f"/countries/{country_name}")
    
    def get_country_timeseries(self, country_name: str) -> Dict:
        """
        Get historical vaccination data for a country.
        
        Args:
            country_name: Name of the country
            
        Returns:
            Dictionary with time series data
            
        Example:
            >>> data = api.get_country_timeseries("India")
            >>> for entry in data['data'][:5]:
            >>>     print(f"{entry['date']}: {entry['total_vaccinations']:,}")
        """
        return self._request("GET", f"/countries/{country_name}/timeseries")
    
    # ==================== Forecasting ====================
    
    def get_forecast(self, country_name: str, days: int = 30) -> Dict:
        """
        Generate an ML-based vaccination forecast for a country.
        
        Args:
            country_name: Name of the country
            days: Number of days to forecast (default: 30)
            
        Returns:
            Dictionary with forecast data
            
        Example:
            >>> forecast = api.get_forecast("India", days=30)
            >>> for day in forecast['forecast'][:5]:
            >>>     print(f"{day['ds']}: {day['yhat']:.0f} doses")
        """
        params = {"days": days}
        return self._request("GET", f"/forecast/{country_name}", params=params)
    
    # ==================== AI Chatbot ====================
    
    def chat(self, message: str, language: str = "en") -> str:
        """
        Chat with the AI Health Assistant.
        
        Args:
            message: Your question or message
            language: Language code (en, hi, bn, ta, te)
            
        Returns:
            AI response message
            
        Example:
            >>> response = api.chat("Is the vaccine safe?")
            >>> print(response)
        """
        payload = {
            "message": message,
            "language": language
        }
        response = self._request("POST", "/chat", json=payload)
        return response.get("message", "")
    
    def get_supported_languages(self) -> List[str]:
        """
        Get the list of supported languages for the chatbot.
        
        Returns:
            List of language codes
        """
        response = self._request("GET", "/chat/languages")
        return response.get("languages", [])
    
    # ==================== Convenience Methods ====================
    
    def compare_countries(self, country1: str, country2: str) -> Dict:
        """
        Compare vaccination statistics between two countries.
        
        Args:
            country1: First country name
            country2: Second country name
            
        Returns:
            Dictionary with comparison data
            
        Example:
            >>> comparison = api.compare_countries("India", "United States")
            >>> print(comparison)
        """
        data1 = self.get_country(country1)
        data2 = self.get_country(country2)
        
        return {
            "country1": {
                "name": country1,
                "data": data1
            },
            "country2": {
                "name": country2,
                "data": data2
            },
            "comparison": {
                "vaccination_rate_difference": data1.get("pct_vaccinated", 0) - data2.get("pct_vaccinated", 0),
                "total_doses_difference": data1.get("total_vaccinations", 0) - data2.get("total_vaccinations", 0)
            }
        }
    
    def search_countries(self, query: str) -> List[str]:
        """
        Search for countries by name.
        
        Args:
            query: Search query (case-insensitive)
            
        Returns:
            List of matching country names
            
        Example:
            >>> results = api.search_countries("united")
            >>> print(results)
            ['United Kingdom', 'United States', 'United Arab Emirates']
        """
        countries = self.get_countries()
        query_lower = query.lower()
        return [c for c in countries if query_lower in c.lower()]


# Convenience function for quick access
def create_client(api_key: str, **kwargs) -> VaccineTrackerAPI:
    """
    Create a new API client instance.
    
    Args:
        api_key: Your API key
        **kwargs: Additional arguments passed to VaccineTrackerAPI
        
    Returns:
        VaccineTrackerAPI instance
    """
    return VaccineTrackerAPI(api_key, **kwargs)


__version__ = "1.0.0"
__all__ = ["VaccineTrackerAPI", "create_client"]
