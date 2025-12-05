"""
Quick verification script for cache warming performance
Tests the actual performance improvement of cache warming
"""
import asyncio
import time
import sys
import os
import requests

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.cache import clear_cache, get_cache_stats
from app.api.cache_warmer import warm_forecast_cache

API_URL = "http://localhost:8001"
API_KEY = "sk_live_d2a632632283fe37f27158c5c830a33f"  # Generated for performance testing

def test_api_available():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def measure_forecast_time(country: str, days: int = 30) -> float:
    """Measure time to get forecast"""
    try:
        start = time.time()
        response = requests.get(
            f"{API_URL}/api/v1/forecast/{country}",
            headers={"X-API-Key": API_KEY},
            params={"days": days},
            timeout=10
        )
        duration = time.time() - start
        
        if response.status_code == 200:
            return duration
        else:
            print(f"  ⚠️ API returned status {response.status_code}")
            return -1
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return -1


async def main():
    """Main verification script"""
    print("=" * 70)
    print("CACHE WARMING PERFORMANCE VERIFICATION")
    print("=" * 70)
    print()
    
    # Check if API is running
    if not test_api_available():
        print("❌ API is not running!")
        print("   Start it with: python -m uvicorn app.api.main:app --port 8001")
        return
    
    print("✅ API is running")
    print()
    
    # Test countries
    test_countries = ['United States', 'India', 'Brazil', 'United Kingdom']
    
    # Test 1: Cold cache performance
    print("📊 Test 1: Cold Cache Performance")
    print("-" * 70)
    clear_cache()
    print("Cache cleared")
    
    cold_times = []
    for country in test_countries[:2]:  # Test 2 countries
        print(f"Testing '{country}'...", end=" ")
        duration = measure_forecast_time(country)
        if duration > 0:
            cold_times.append(duration)
            print(f"{duration*1000:.0f}ms")
        else:
            print("FAILED")
    
    avg_cold = sum(cold_times) / len(cold_times) if cold_times else 0
    print(f"\n  Average cold cache time: {avg_cold*1000:.0f}ms")
    print()
    
    # Test 2: Warm the cache
    print("🔥 Test 2: Warming Cache")
    print("-" * 70)
    clear_cache()
    
    start = time.time()
    stats = await warm_forecast_cache(countries=test_countries, max_concurrent=2)
    warming_duration = time.time() - start
    
    print(f"Cache warmed: {stats['successful']}/{stats['total_countries']} successful")
    print(f"Warming took: {warming_duration:.1f}s")
    print()
    
    # Test 3: Warm cache performance
    print("⚡ Test 3: Warm Cache Performance")
    print("-" * 70)
    
    warm_times = []
    for country in test_countries:
        print(f"Testing '{country}'...", end=" ")
        duration = measure_forecast_time(country)
        if duration > 0:
            warm_times.append(duration)
            status = "✓" if duration < 0.1 else "⚠"
            print(f"{duration*1000:.0f}ms {status}")
        else:
            print("FAILED")
    
    avg_warm = sum(warm_times) / len(warm_times) if warm_times else 0
    print(f"\n  Average warm cache time: {avg_warm*1000:.0f}ms")
    print()
    
    # Results
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    if avg_cold > 0 and avg_warm > 0:
        improvement = ((avg_cold - avg_warm) / avg_cold) * 100
        speedup = avg_cold / avg_warm
        
        print(f"Cold cache:      {avg_cold*1000:.0f}ms")
        print(f"Warm cache:      {avg_warm*1000:.0f}ms")
        print(f"Improvement:     {improvement:.1f}% faster")
        print(f"Speedup:         {speedup:.1f}x")
        print()
        
        if improvement >= 95:
            print("✅ EXCELLENT: Achieved 95%+ performance improvement!")
        elif improvement >= 90:
            print("✅ GOOD: Achieved 90%+ performance improvement!")
        else:
            print(f"⚠️ MODERATE: {improvement:.1f}% improvement (target: 95%+)")
    else:
        print("⚠️ Could not complete performance comparison")
    
    print()
    
    # Cache stats
    try:
        cache_stats = get_cache_stats()
        print("Cache Statistics:")
        print(f"  Backend: {cache_stats.get('backend', 'unknown')}")
        print(f"  Memory keys: {cache_stats.get('memory_keys', 0)}")
        if 'redis_keys' in cache_stats:
            print(f"  Redis keys: {cache_stats.get('redis_keys', 0)}")
            print(f"  Redis hits: {cache_stats.get('redis_hits', 0)}")
            print(f"  Redis misses: {cache_stats.get('redis_misses', 0)}")
    except Exception as e:
        print(f"  Could not get cache stats: {e}")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
