from redis.asyncio import Redis, from_url

from core.config import settings


def get_redis_cache() -> Redis:
    """Connects to Redis using url from settings.

    Returns:
        Redis: Redis client to connect.
    """

    return from_url(settings.redis_cache.redis_url.unicode_string())
