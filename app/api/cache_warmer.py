"""
Cache Warming Utility for Prophet Forecasting
Precomputes forecasts for popular countries to achieve 99% performance improvement
"""
import asyncio
import logging
import time
from typing import List
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.storage import get_country_timeseries, get_latest_by_country
from src.forecast import fit_prophet_for_country
from app.api.cache import set_in_cache, cache_key

# Setup logging
logger = logging.getLogger(__name__)

# Popular countries to warm cache for (top 15 by global importance)
POPULAR_COUNTRIES = [
    'United States',
    'India', 
    'Brazil',
    'United Kingdom',
    'Germany',
    'France',
    'Italy',
    'Spain',
    'Canada',
    'Japan',
    'South Korea',
    'Australia',
    'Mexico',
    'Argentina',
    'Russia'
]

# Default forecast parameters
DEFAULT_FORECAST_DAYS = 30
DEFAULT_FORECAST_METRIC = 'total_vaccinations'
CACHE_TTL = 7200  # 2 hours (matches route cache TTL)


def get_popular_countries_from_db(limit: int = 15) -> List[str]:
    """
    Dynamically fetch top countries by vaccination coverage from database.
    
    Args:
        limit: Number of top countries to return
        
    Returns:
        List of country names
    """
    try:
        df = get_latest_by_country(limit=limit)
        countries = df['location'].tolist()
        logger.info(f"Fetched {len(countries)} popular countries from database")
        return countries
    except Exception as e:
        logger.warning(f"Could not fetch countries from DB: {e}. Using static list.")
        return POPULAR_COUNTRIES[:limit]


async def warm_single_country(country: str, days: int = DEFAULT_FORECAST_DAYS, 
                               metric: str = DEFAULT_FORECAST_METRIC) -> bool:
    """
    Warm cache for a single country's forecast.
    
    Args:
        country: Country name
        days: Number of days to forecast
        metric: Metric to forecast (e.g., 'total_vaccinations')
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get historical data
        df = get_country_timeseries(country)
        
        if df is None or df.empty:
            logger.warning(f"No data available for '{country}', skipping")
            return False
        
        if metric not in df.columns:
            logger.warning(f"Metric '{metric}' not found for '{country}', skipping")
            return False
        
        # Generate forecast (this is the expensive operation)
        forecast_df = fit_prophet_for_country(df, column=metric, periods=days)
        
        if forecast_df is None or forecast_df.empty:
            logger.warning(f"Failed to generate forecast for '{country}'")
            return False
        
        # Convert forecast to cache format (matching route response structure)
        forecast_points = []
        for _, row in forecast_df.iterrows():
            forecast_points.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted_value': float(row['yhat']),
                'lower_bound': float(row['yhat_lower']) if 'yhat_lower' in row else None,
                'upper_bound': float(row['yhat_upper']) if 'yhat_upper' in row else None
            })
        
        # Build response matching ForecastResponse model
        response_data = {
            'country': country,
            'metric': metric,
            'forecast_days': days,
            'forecast': forecast_points
        }
        
        # Generate cache key matching the route's cache key format
        # The route uses: @cached decorator which creates key from function args
        # We need to match: get_forecast(country_name, days, metric)
        key = f"get_forecast:{cache_key(country, days, metric)}"
        
        # Store in cache
        set_in_cache(key, response_data, ttl=CACHE_TTL)
        
        logger.info(f"✅ Cache warmed for '{country}' ({days} days, {metric})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to warm cache for '{country}': {str(e)}")
        return False


async def warm_forecast_cache(countries: List[str] = None, 
                               use_db_countries: bool = False,
                               max_concurrent: int = 3) -> dict:
    """
    Warm forecast cache for multiple countries concurrently.
    
    Args:
        countries: List of country names to warm. If None, uses POPULAR_COUNTRIES
        use_db_countries: If True, fetch top countries from database instead
        max_concurrent: Maximum number of concurrent warming tasks
        
    Returns:
        Dictionary with warming statistics
    """
    start_time = time.time()
    
    # Determine which countries to warm
    if countries is None:
        if use_db_countries:
            countries = get_popular_countries_from_db()
        else:
            countries = POPULAR_COUNTRIES
    
    logger.info(f"🔥 Starting cache warming for {len(countries)} countries...")
    
    # Warm caches with controlled concurrency
    # We limit concurrency because Prophet training is CPU-intensive
    success_count = 0
    failure_count = 0
    
    # Process in batches to limit concurrent operations
    for i in range(0, len(countries), max_concurrent):
        batch = countries[i:i + max_concurrent]
        tasks = [warm_single_country(country) for country in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, bool) and result:
                success_count += 1
            else:
                failure_count += 1
    
    duration = time.time() - start_time
    
    stats = {
        'total_countries': len(countries),
        'successful': success_count,
        'failed': failure_count,
        'duration_seconds': round(duration, 2)
    }
    
    logger.info(f"✨ Cache warming completed in {duration:.1f}s")
    logger.info(f"   Successful: {success_count}/{len(countries)}")
    logger.info(f"   Failed: {failure_count}/{len(countries)}")
    
    return stats


if __name__ == "__main__":
    # Test cache warming standalone
    import asyncio
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Testing cache warming...")
    print("=" * 70)
    
    # Test with a few countries
    test_countries = ['United States', 'India', 'Brazil']
    
    stats = asyncio.run(warm_forecast_cache(countries=test_countries))
    
    print("\n" + "=" * 70)
    print("Cache warming test results:")
    print(f"  Total: {stats['total_countries']}")
    print(f"  Successful: {stats['successful']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Duration: {stats['duration_seconds']}s")
    print("=" * 70)
