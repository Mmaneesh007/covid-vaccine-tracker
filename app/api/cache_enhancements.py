"""
Advanced Cache Warming Features
- Scheduled background refresh
- ETL-triggered cache warming
- Dynamic popular countries selection based on API metrics
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.api.cache_warmer import warm_forecast_cache, POPULAR_COUNTRIES
from app.api.cache import invalidate_key

logger = logging.getLogger(__name__)

# Configuration
REFRESH_INTERVAL_HOURS = 2  # Refresh cache every 2 hours
API_METRICS_WINDOW_HOURS = 24  # Look at last 24 hours of API calls


class CacheRefreshScheduler:
    """Manages scheduled cache refresh"""
    
    def __init__(self, interval_hours: int = REFRESH_INTERVAL_HOURS):
        self.interval_hours = interval_hours
        self.is_running = False
        self.task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the scheduled refresh loop"""
        if self.is_running:
            logger.warning("Cache refresh scheduler is already running")
            return
        
        self.is_running = True
        logger.info(f"🕐 Starting cache refresh scheduler (every {self.interval_hours}h)")
        
        while self.is_running:
            try:
                # Wait for the interval
                await asyncio.sleep(self.interval_hours * 3600)
                
                if not self.is_running:
                    break
                
                logger.info("🔄 Scheduled cache refresh triggered")
                
                # Invalidate old forecast caches before refreshing
                invalidate_key("get_forecast:*")
                
                # Warm the cache again
                stats = await warm_forecast_cache(use_db_countries=True)
                logger.info(f"✨ Scheduled refresh complete: {stats}")
                
            except asyncio.CancelledError:
                logger.info("Cache refresh scheduler cancelled")
                break
            except Exception as e:
                logger.error(f"Error in cache refresh scheduler: {e}")
                # Continue running even if one refresh fails
    
    async def stop(self):
        """Stop the scheduled refresh loop"""
        logger.info("Stopping cache refresh scheduler...")
        self.is_running = False
        
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
    
    def start_background(self):
        """Start scheduler as background task"""
        self.task = asyncio.create_task(self.start())
        return self.task


# Global scheduler instance
_scheduler: Optional[CacheRefreshScheduler] = None


def get_scheduler() -> CacheRefreshScheduler:
    """Get or create the global scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = CacheRefreshScheduler()
    return _scheduler


async def trigger_cache_refresh(reason: str = "Manual trigger"):
    """
    Manually trigger cache refresh (e.g., after ETL update)
    
    Args:
        reason: Reason for triggering refresh (for logging)
    """
    logger.info(f"🔥 Manual cache refresh triggered: {reason}")
    
    try:
        # Invalidate old forecasts
        invalidate_key("get_forecast:*")
        
        # Warm cache with fresh data
        stats = await warm_forecast_cache(use_db_countries=True)
        
        logger.info(f"✨ Manual refresh complete: {stats}")
        return stats
    
    except Exception as e:
        logger.error(f"Manual cache refresh failed: {e}")
        raise


def get_dynamic_popular_countries(limit: int = 15, min_api_calls: int = 5) -> List[str]:
    """
    Get popular countries based on actual API usage metrics
    
    Args:
        limit: Maximum number of countries to return
        min_api_calls: Minimum API calls to consider a country popular
        
    Returns:
        List of country names sorted by popularity
        
    Note:
        This is a placeholder implementation. In production, you would:
        1. Track API calls to /forecast/{country} in a database or metrics system
        2. Query that data to get actual popular countries
        3. Fall back to static list if metrics unavailable
    """
    try:
        # TODO: Replace with actual API metrics query
        # Example implementation:
        # from app.api.metrics import get_forecast_call_counts
        # country_calls = get_forecast_call_counts(hours=API_METRICS_WINDOW_HOURS)
        # popular = [country for country, calls in country_calls.items() if calls >= min_api_calls]
        # return sorted(popular, key=lambda c: country_calls[c], reverse=True)[:limit]
        
        # For now, use database-based popular countries
        from src.storage import get_latest_by_country
        
        df = get_latest_by_country(limit=limit)
        countries = df['location'].tolist()
        
        logger.info(f"📊 Dynamic popular countries (DB-based): {len(countries)} countries")
        return countries
        
    except Exception as e:
        logger.warning(f"Could not get dynamic popular countries: {e}. Using static list.")
        return POPULAR_COUNTRIES[:limit]


# ETL Integration Hook
async def on_etl_complete():
    """
    Hook to call after ETL pipeline completes
    Triggers cache refresh with new data
    
    Usage:
        from app.api.cache_enhancements import on_etl_complete
        
        # In your ETL script after data update:
        import asyncio
        asyncio.run(on_etl_complete())
    """
    logger.info("📥 ETL pipeline completed - triggering cache refresh")
    return await trigger_cache_refresh(reason="ETL data update")


if __name__ == "__main__":
    # Test the scheduler
    import asyncio
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    async def test_scheduler():
        print("Testing Cache Refresh Scheduler")
        print("=" * 70)
        
        # Test 1: Manual trigger
        print("\nTest 1: Manual Trigger")
        print("-" * 70)
        stats = await trigger_cache_refresh(reason="Test trigger")
        print(f"Result: {stats}")
        
        # Test 2: Dynamic popular countries
        print("\nTest 2: Dynamic Popular Countries")
        print("-" * 70)
        countries = get_dynamic_popular_countries(limit=5)
        print(f"Popular countries: {countries}")
        
        # Test 3: Scheduler (just start and stop immediately)
        print("\nTest 3: Scheduler Start/Stop")
        print("-" * 70)
        scheduler = get_scheduler()
        scheduler.start_background()
        print("Scheduler started")
        
        await asyncio.sleep(2)  # Let it run briefly
        
        await scheduler.stop()
        print("Scheduler stopped")
        
        print("\n" + "=" * 70)
        print("All tests completed!")
    
    asyncio.run(test_scheduler())
