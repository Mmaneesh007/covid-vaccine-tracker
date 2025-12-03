"""
Enhanced caching layer with Redis support and in-memory fallback
Automatically falls back to in-memory cache if Redis is unavailable
"""
from functools import wraps
import hashlib
import json
import time
from typing import Any, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Redis
try:
    import redis
    from redis import ConnectionPool
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not installed. Using in-memory cache only.")

# Cache storage
_memory_cache = {}
_cache_timestamps = {}
_redis_client: Optional['redis.Redis'] = None

# Default TTL: 1 hour
DEFAULT_TTL = 3600

# Redis connection settings
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0


def init_redis(host: str = REDIS_HOST, port: int = REDIS_PORT, db: int = REDIS_DB):
    """
    Initialize Redis connection
    Falls back gracefully if Redis is unavailable
    """
    global _redis_client
    
    if not REDIS_AVAILABLE:
        logger.info("Redis library not available. Using in-memory cache.")
        return False
    
    try:
        pool = ConnectionPool(host=host, port=port, db=db, decode_responses=True)
        _redis_client = redis.Redis(connection_pool=pool)
        # Test connection
        _redis_client.ping()
        logger.info(f"✅ Redis connected at {host}:{port}")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Could not connect to Redis: {e}. Falling back to in-memory cache.")
        _redis_client = None
        return False


def cache_key(*args, **kwargs) -> str:
    """Generate a cache key from function arguments"""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()


def get_from_cache(key: str) -> Optional[Any]:
    """Get value from cache (Redis or memory)"""
    # Try Redis first
    if _redis_client:
        try:
            value = _redis_client.get(key)
            if value:
                logger.info(f"[REDIS] HIT: {key[:20]}...")
                return json.loads(value)
        except Exception as e:
            logger.error(f"[REDIS] Error: {e}")
    
    # Fallback to memory cache
    if key in _memory_cache:
        timestamp = _cache_timestamps.get(key, 0)
        # Check if still valid (we handle TTL manually for memory cache)
        logger.info(f"[MEMORY] HIT: {key[:20]}...")
        return _memory_cache[key]
    
    return None


def set_in_cache(key: str, value: Any, ttl: int = DEFAULT_TTL):
    """Set value in cache (Redis or memory)"""
    # Try Redis first
    if _redis_client:
        try:
            _redis_client.setex(key, ttl, json.dumps(value))
            logger.info(f"[REDIS] SET: {key[:20]}... (TTL: {ttl}s)")
            return
        except Exception as e:
            logger.error(f"[REDIS] Error: {e}")
    
    # Fallback to memory cache
    _memory_cache[key] = value
    _cache_timestamps[key] = time.time() + ttl  # Store expiry time
    logger.info(f"[MEMORY] SET: {key[:20]}... (TTL: {ttl}s)")


def is_expired(key: str) -> bool:
    """Check if a memory cache key is expired"""
    if key not in _cache_timestamps:
        return True
    return time.time() > _cache_timestamps[key]


def cached(ttl: int = DEFAULT_TTL):
    """
    Cache decorator with Redis support and in-memory fallback
    
    Args:
        ttl: Time to live in seconds
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = get_from_cache(key)
            
            # Check memory cache expiry
            if cached_value is not None and key in _memory_cache:
                if is_expired(key):
                    logger.info(f"[CACHE] EXPIRED: {func.__name__}")
                    del _memory_cache[key]
                    del _cache_timestamps[key]
                    cached_value = None
            
            if cached_value is not None:
                return cached_value
            
            # Cache miss - call function
            logger.info(f"[CACHE] MISS: {func.__name__}")
            result = await func(*args, **kwargs)
            
            # Store in cache
            set_in_cache(key, result, ttl)
            
            return result
        return wrapper
    return decorator


def clear_cache():
    """Clear all cached data (Redis and memory)"""
    global _memory_cache, _cache_timestamps
    
    # Clear Redis
    if _redis_client:
        try:
            _redis_client.flushdb()
            logger.info("[REDIS] Cleared")
        except Exception as e:
            logger.error(f"[REDIS] Clear error: {e}")
    
    # Clear memory
    _memory_cache.clear()
    _cache_timestamps.clear()
    logger.info("[MEMORY] Cleared")


def invalidate_key(pattern: str):
    """Invalidate cache keys matching a pattern"""
    if _redis_client:
        try:
            keys = _redis_client.keys(pattern)
            if keys:
                _redis_client.delete(*keys)
                logger.info(f"[REDIS] Invalidated {len(keys)} keys matching '{pattern}'")
        except Exception as e:
            logger.error(f"[REDIS] Invalidate error: {e}")
    
    # Memory cache pattern matching
    matching_keys = [k for k in _memory_cache.keys() if pattern in k]
    for k in matching_keys:
        del _memory_cache[k]
        if k in _cache_timestamps:
            del _cache_timestamps[k]
    
    if matching_keys:
        logger.info(f"[MEMORY] Invalidated {len(matching_keys)} keys matching '{pattern}'")


def get_cache_stats():
    """Get cache statistics"""
    stats = {
        "backend": "redis" if _redis_client else "memory",
        "memory_keys": len(_memory_cache),
        "memory_usage_mb": sum(len(str(v)) for v in _memory_cache.values()) / 1024 / 1024,
    }
    
    if _redis_client:
        try:
            info = _redis_client.info("stats")
            stats["redis_keys"] = _redis_client.dbsize()
            stats["redis_hits"] = info.get("keyspace_hits", 0)
            stats["redis_misses"] = info.get("keyspace_misses", 0)
        except Exception as e:
            logger.error(f"[REDIS] Stats error: {e}")
    
    return stats


# Auto-initialize Redis on import
init_redis()
