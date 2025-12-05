"""
Test cache warming functionality
"""
import pytest
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.cache_warmer import (
    warm_single_country,
    warm_forecast_cache,
    get_popular_countries_from_db,
    POPULAR_COUNTRIES
)
from app.api.cache import get_from_cache, clear_cache, cache_key


class TestCacheWarmer:
    """Test cache warming functionality"""
    
    def setup_method(self):
        """Clear cache before each test"""
        clear_cache()
    
    @pytest.mark.asyncio
    async def test_warm_single_country_success(self):
        """Test warming cache for a single country"""
        # Test with a country that should have data
        result = await warm_single_country('United States', days=30)
        
        # Should succeed
        assert result is True
        
        # Verify data is in cache
        key = f"get_forecast:{cache_key('United States', 30, 'total_vaccinations')}"
        cached_data = get_from_cache(key)
        
        assert cached_data is not None
        assert cached_data['country'] == 'United States'
        assert cached_data['forecast_days'] == 30
        assert len(cached_data['forecast']) > 0
    
    @pytest.mark.asyncio
    async def test_warm_single_country_nonexistent(self):
        """Test warming cache for non-existent country"""
        # Test with a country that doesn't exist
        result = await warm_single_country('FakeCountryXYZ', days=30)
        
        # Should fail gracefully
        assert result is False
    
    @pytest.mark.asyncio
    async def test_warm_multiple_countries(self):
        """Test warming cache for multiple countries"""
        test_countries = ['United States', 'India', 'Brazil']
        
        stats = await warm_forecast_cache(countries=test_countries, max_concurrent=2)
        
        # Verify statistics
        assert stats['total_countries'] == 3
        assert stats['successful'] >= 1  # At least one should succeed
        assert stats['successful'] + stats['failed'] == 3
        assert stats['duration_seconds'] > 0
    
    @pytest.mark.asyncio
    async def test_concurrent_warming(self):
        """Test that concurrent warming works correctly"""
        import time
        
        test_countries = ['United States', 'India']
        
        start = time.time()
        stats = await warm_forecast_cache(countries=test_countries, max_concurrent=2)
        duration = time.time() - start
        
        # With concurrent warming, should be faster than sequential
        # (though not testable without comparison, we check it completes)
        assert stats['successful'] >= 1
        print(f"Concurrent warming took {duration:.2f}s")
    
    def test_popular_countries_list(self):
        """Test that popular countries list is properly defined"""
        assert isinstance(POPULAR_COUNTRIES, list)
        assert len(POPULAR_COUNTRIES) > 0
        assert 'United States' in POPULAR_COUNTRIES
        assert 'India' in POPULAR_COUNTRIES
    
    def test_get_popular_countries_from_db(self):
        """Test fetching popular countries from database"""
        countries = get_popular_countries_from_db(limit=5)
        
        assert isinstance(countries, list)
        assert len(countries) > 0
        assert len(countries) <= 5


@pytest.mark.skipif(
    not os.path.exists('data/vax_tracker.db'),
    reason="Database not found - run ETL pipeline first"
)
class TestCacheWarmerIntegration:
    """Integration tests requiring database"""
    
    @pytest.mark.asyncio
    async def test_full_cache_warming(self):
        """Test full cache warming with all popular countries"""
        # Use static list for predictable testing
        stats = await warm_forecast_cache(use_db_countries=False)
        
        assert stats['total_countries'] == len(POPULAR_COUNTRIES)
        assert stats['successful'] >= 5  # At least some should succeed
        print(f"\nCache warming stats: {stats}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, '-v', '--tb=short'])
