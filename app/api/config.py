"""
Configuration for Experimental FastAPI Backend
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    app_name: str = "COVID-19 Vaccine Tracker API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True
    
    # CORS Settings - Allow Streamlit Cloud and localhost
    cors_origins: list = [
        "https://covid-vaccine-tracker-2025.streamlit.app",
        "http://localhost:8501",
        "http://localhost:3000",
        "*"  # Allow all for public API testing
    ]
    
    # Database Settings (reuse existing SQLite)
    database_url: str = "sqlite:///./data/vax_tracker.db"
    
    # Cache Settings
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour in seconds
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
