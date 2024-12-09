from redis.asyncio import Redis, from_url

from core.config import settings


class RedisClient:
    """A class to manage connection to Redis database."""

    def __init__(self, url: str) -> None:
        """Inits Redis client from given.

        Args:
            url (str): URL to connect to redis
        """

        self.client = from_url(url)

    def get_client(self) -> Redis:
        """Returns Redis client to connect.

        Returns:
            Redis: Redis client to connect
        """

        return self.client


redis_client = RedisClient(settings.redis_cache.redis_url.unicode_string())
