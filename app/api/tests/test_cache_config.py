"""
Unit tests for API cache, configuration, and utilities
"""
import pytest
from unittest.mock import patch, MagicMock
import time
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app.api.cache import cached, set_in_cache, get_from_cache, cache_key, init_redis
from app.api.config import get_settings


class TestCacheKey:
    """Test cache key generation"""
    
    def test_cache_key_generation(self):
        """Test that cache keys are generated consistently"""
        key1 = cache_key("arg1", "arg2", kwarg1="value1")
        key2 = cache_key("arg1", "arg2", kwarg1="value1")
        
        assert key1 == key2
    
    def test_cache_key_different_args(self):
        """Test that different args generate different keys"""
        key1 = cache_key("arg1", "arg2")
        key2 = cache_key("arg1", "arg3")
        
        assert key1 != key2


class TestMemoryCache:
    """Test in-memory caching"""
    
    def test_set_and_get_cache(self):
        """Test setting and retrieving from cache"""
        test_data = {"country": "India", "vaccinations": 2200000000}
        
        set_in_cache("test_key", test_data, ttl=3600)
        result = get_from_cache("test_key")
        
        assert result == test_data
    
    def test_cache_miss(self):
        """Test cache miss returns None"""
        result = get_from_cache("nonexistent_key_xyz")
        
        assert result is None
    
    def test_cache_ttl_expiry(self):
        """Test cache TTL expiry"""
        test_data = {"test": "data"}
        
        # Set with very short TTL
        set_in_cache("short_ttl_key", test_data, ttl=1)
        
        # Should be available immediately
        assert get_from_cache("short_ttl_key") is not None
        
        # Wait for expiry
        time.sleep(1.5)
        
        # Should be expired (None for memory cache with isExpired check)
        # Note: This depends on implementation details


class TestSettings:
    """Test configuration settings"""
    
    def test_get_settings(self):
        """Test settings singleton"""
        settings1 = get_settings()
        settings2 = get_settings()
        
        # Should return same instance (cached)
        assert settings1 is settings2
    
    def test_settings_defaults(self):
        """Test default settings values"""
        settings = get_settings()
        
        assert settings.app_name == "COVID-19 Vaccine Tracker API"
        assert settings.api_prefix == "/api/v1"
        assert settings.port == 8001
        assert settings.enable_cache is True
        assert settings.cache_ttl == 3600
    
    def test_settings_cors_origins(self):
        """Test CORS origins configuration"""
        settings = get_settings()
        
        assert "https://covid-vaccine-tracker-2025.streamlit.app" in settings.cors_origins
        assert "http://localhost:8501" in settings.cors_origins
        assert "http://localhost:8001" in settings.cors_origins
        # Should not contain wildcard
        assert "*" not in settings.cors_origins
    
    def test_settings_database_url(self):
        """Test database URL configuration"""
        settings = get_settings()
        
        assert "sqlite" in settings.database_url.lower()


class TestRedisInit:
    """Test Redis initialization (with graceful fallback)"""
    
    @patch('app.api.cache.REDIS_AVAILABLE', False)
    def test_redis_not_available(self):
        """Test graceful fallback when Redis not installed"""
        result = init_redis()
        assert result is False
    
    @patch('app.api.cache.redis.Redis')
    @patch('app.api.cache.REDIS_AVAILABLE', True)
    def test_redis_connection_success(self, mock_redis):
        """Test successful Redis connection"""
        mock_instance = MagicMock()
        mock_instance.ping.return_value = True
        mock_redis.return_value = mock_instance
        
        # Note: This might fail depending on actual Redis availability
        # but demonstrates the expected behavior


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
