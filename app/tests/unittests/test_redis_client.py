from unittest.mock import AsyncMock, MagicMock, patch

from redis.asyncio import Redis

from core.redis.redis_cache import RedisClient


def test_redis_client():
    """Tests RedisClient."""

    mock_redis = AsyncMock(spec=Redis)
    mock_from_url = MagicMock(return_value=mock_redis)
    mock_redis_url = "redis://mock_host@mock_port/mock_db"

    with patch("core.redis.redis_cache.from_url", mock_from_url):
        redis_client = RedisClient(mock_redis_url)
        result = redis_client.get_client()

        mock_from_url.assert_called_once_with(mock_redis_url)

        assert result == mock_redis
