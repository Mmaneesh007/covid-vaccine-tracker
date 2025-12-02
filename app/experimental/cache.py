"""
Simple in-memory caching middleware for FastAPI
No Redis required - uses Python dict for basic caching
"""
from functools import wraps
import hashlib
import json
import time
from typing import Any, Optional

# Simple in-memory cache
_cache = {}
_cache_timestamps = {}

# Default TTL: 1 hour
DEFAULT_TTL = 3600


def cache_key(*args, **kwargs) -> str:
    """Generate a cache key from function arguments"""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()


def cached(ttl: int = DEFAULT_TTL):
    """
    Simple cache decorator (in-memory, no Redis needed)
    
    Args:
        ttl: Time to live in seconds
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Check if in cache and not expired
            if key in _cache:
                timestamp = _cache_timestamps.get(key, 0)
                if time.time() - timestamp < ttl:
                    print(f"[CACHE] HIT: {func.__name__}")
                    return _cache[key]
            
            # Not in cache or expired - call function
            print(f"[CACHE] MISS: {func.__name__}")
            result = await func(*args, **kwargs)
            
            # Store in cache
            _cache[key] = result
            _cache_timestamps[key] = time.time()
            
            return result
        return wrapper
    return decorator


def clear_cache():
    """Clear all cached data"""
    global _cache, _cache_timestamps
    _cache.clear()
    _cache_timestamps.clear()
    print("[CACHE] Cleared")


def get_cache_stats():
    """Get cache statistics"""
    return {
        "total_keys": len(_cache),
        "memory_usage_mb": sum(len(str(v)) for v in _cache.values()) / 1024 / 1024
    }
