from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


async def clear_cache_task() -> None:
    """Clears cache from Redis."""

    cache_backend = FastAPICache.get_backend()
    if isinstance(cache_backend, RedisBackend):
        redis = cache_backend.redis
        await redis.flushdb()
