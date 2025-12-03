# ⚡ Performance Optimizations

This document describes the caching strategy implemented to improve API response times.

---

## 🚀 Caching Strategy

The API uses **Redis** for distributed caching with automatic fallback to **in-memory caching** if Redis is unavailable.

### Cached Endpoints

| Endpoint | TTL | Benefit |
|:---------|:----|:--------|
| `GET /countries` | 1 hour | Reduces DB queries for country list |
| `GET /countries/{name}` | 30 min | Caches individual country stats |
| `GET /forecast/{name}` | 2 hours | Expensive ML operations cached |
| `GET /global` | 1 hour | Aggregated stats cached |
| `GET /top` | 1 hour | Sorted country rankings cached |

### Cache Invalidation

**Automatic**: Cached data expires based on TTL (Time To Live).

**Manual**:

```python
from app.experimental.cache import clear_cache, invalidate_key

# Clear all cache
clear_cache()

# Invalidate specific pattern
invalidate_key("get_country_stats:*")
```

---

## 🔧 Redis Setup (Optional)

### Windows

1. **Download Redis**:
   - Use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) or
   - [Memurai](https://www.memurai.com/) (Windows-native Redis)

2. **Start Redis**:

```bash
# Using WSL
wsl -d Ubuntu
sudo service redis-server start

# Or Memurai (runs as Windows service)
```

3. **Verify**:

```bash
redis-cli ping
# Should return: PONG
```

### macOS/Linux

```bash
# Install
brew install redis  # macOS
sudo apt install redis-server  # Ubuntu

# Start
redis-server

# Verify
redis-cli ping
```

---

## 📊 Performance Benchmarks

### Without Cache (Cold Start)

| Endpoint | Response Time |
|:--|:--|
| `GET /countries` | ~150ms |
| `GET /countries/India` | ~80ms |
| `GET /forecast/USA` | ~2,500ms |

### With Cache (Warm)

| Endpoint | Response Time | Improvement |
|:--|:--|:--|
| `GET /countries` | ~5ms | **97% faster** |
| `GET /countries/India` | ~3ms | **96% faster** |
| `GET /forecast/USA` | ~10ms | **99.6% faster** |

> **Note**: Forecasting is especially slow due to Prophet ML model training. Caching reduces this from seconds to milliseconds!

---

## 🔍 Cache Statistics

Access cache stats via the `/health` endpoint:

```json
{
  "status": "healthy",
  "cache": {
    "backend": "redis",
    "redis_keys": 42,
    "redis_hits": 1523,
    "redis_misses": 89
  }
}
```

---

## 🛠️ Graceful Degradation

The system automatically falls back to in-memory caching if:

- Redis is not installed
- Redis server is not running
- Redis connection fails

**No configuration needed** - it "just works"!

---

## 📦 Dependencies

```bash
pip install redis==5.0.1
```

Already included in `app/experimental/requirements-api.txt`.

---

## 🧪 Testing Cache Behavior

### Test Redis Connection

```python
from app.experimental.cache import get_cache_stats

stats = get_cache_stats()
print(stats)  # Shows 'redis' or 'memory' backend
```

### Force Cache Miss

```python
from app.experimental.cache import clear_cache

clear_cache()  # Next request will be slow (cache miss)
# Subsequent request will be fast (cache hit)
```

---

## 💡 Best Practices

1. **Longer TTL for expensive operations**: Forecasts (2 hours) vs Stats (30 min)
2. **Invalidate on data updates**: If ETL refreshes data, clear cache
3. **Monitor hit rate**: High hit rate = effective caching

---

## 🔮 Future Enhancements

- [ ] Cache warming on startup
- [ ] Distributed caching for multi-instance deployments
- [ ] Compression for large responses
- [ ] Cache hit/miss metrics dashboard
