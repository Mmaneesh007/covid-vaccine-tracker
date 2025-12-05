"""
ETL Integration for Cache Warming
Add this to your run_all.py or ETL pipeline to trigger cache refresh after data update
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def trigger_cache_refresh_after_etl():
    """
    Call this function after ETL pipeline completes to refresh forecast caches
    
    Usage:
        # At the end of run_all.py main() function:
        from etl_cache_hook import trigger_cache_refresh_after_etl
        trigger_cache_refresh_after_etl()
    """
    try:
        from app.api.cache_enhancements import on_etl_complete
        
        print("\n" + "=" * 70)
        print("Triggering cache refresh after ETL update...")
        print("=" * 70)
        
        stats = asyncio.run(on_etl_complete())
        
        print(f"✅ Cache refresh complete:")
        print(f"   Successful: {stats['successful']}/{stats['total_countries']}")
        print(f"   Duration: {stats['duration_seconds']}s")
        print("=" * 70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Cache refresh failed: {e}")
        print("   (This is non-critical - cache will refresh on schedule)")
        return False


if __name__ == "__main__":
    # Test the hook
    trigger_cache_refresh_after_etl()
