"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


# Response Models
class VaccinationStats(BaseModel):
    """Country vaccination statistics"""
    country: str
    total_vaccinations: Optional[int] = Field(None, description="Total vaccine doses administered")
    people_vaccinated: Optional[int] = Field(None, description="Number of people with at least one dose")
    people_fully_vaccinated: Optional[int] = Field(None, description="Number of fully vaccinated people")
    daily_vaccinations: Optional[int] = Field(None, description="Daily vaccination rate")
    total_vaccinations_per_hundred: Optional[float] = Field(None, description="Doses per 100 people")
    people_vaccinated_per_hundred: Optional[float] = Field(None, description="% with at least one dose")
    people_fully_vaccinated_per_hundred: Optional[float] = Field(None, description="% fully vaccinated")
    date: Optional[str] = Field(None, description="Latest data date")
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }


class TimeSeriesPoint(BaseModel):
    """Single time series data point"""
    date: str
    value: Optional[float] = None


class TimeSeriesData(BaseModel):
    """Time series data for a country"""
    country: str
    metric: str
    data: List[TimeSeriesPoint]


class ForecastPoint(BaseModel):
    """Single forecast data point"""
    date: str
    predicted_value: float
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None


class ForecastResponse(BaseModel):
    """Forecast response"""
    country: str
    metric: str
    forecast_days: int
    forecast: List[ForecastPoint]
    
    class Config:
        json_schema_extra = {
            "example": {
                "country": "India",
                "metric": "total_vaccinations",
                "forecast_days": 30,
                "forecast": [
                    {"date": "2024-02-01", "predicted_value": 2250000000, "lower_bound": 2200000000, "upper_bound": 2300000000}
                ]
            }
        }


# Request Models
class ChatRequest(BaseModel):
    """Chatbot request"""
    message: str = Field(..., min_length=1, max_length=500, description="User's message")
    language: str = Field("en", description="Language code (en, hi, bn, ta, te)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Is the COVID vaccine safe?",
                "language": "en"
            }
        }


class ChatResponse(BaseModel):
    """Chatbot response"""
    message: str
    language: str
    sentiment: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Yes, COVID-19 vaccines are safe and effective...",
                "language": "en",
                "sentiment": {"polarity": 0.5, "subjectivity": 0.6}
            }
        }


class CountryListResponse(BaseModel):
    """List of available countries"""
    countries: List[str]
    total_count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    status_code: int
