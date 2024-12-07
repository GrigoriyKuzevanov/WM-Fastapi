from unittest.mock import AsyncMock, MagicMock, patch

from redis.asyncio import Redis

from core.redis import get_redis_cache


def test_get_redis_cache():
    """Tests get_redis_cache function."""

    mock_redis = AsyncMock(spec=Redis)
    mock_from_url = MagicMock(spec="redis.asyncio.from_url", return_value=mock_redis)
    mock_redis_url = "redis://mock_host@mock_port/mock_db"
    mock_settings = MagicMock()

    with (
        patch("core.redis.redis_cache.settings", mock_settings),
        patch("core.redis.redis_cache.from_url", mock_from_url),
    ):
        mock_settings.redis_cache.redis_url.unicode_string.return_value = mock_redis_url
        result = get_redis_cache()

        mock_from_url.assert_called_once_with(mock_redis_url)

        assert result == mock_redis
