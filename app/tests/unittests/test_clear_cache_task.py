from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from core.redis import clear_cache_task


@pytest.mark.asyncio
async def test_with_mock_redis_backend() -> None:
    """Tests "clear_cache_task" clears redis cache backend."""

    mock_backend = MagicMock(spec=RedisBackend)
    mock_backend.redis = AsyncMock()

    with patch.object(FastAPICache, "get_backend", return_value=mock_backend):
        await clear_cache_task()

        mock_backend.redis.flushdb.assert_awaited_once()


@pytest.mark.asyncio
async def test_with_mock_non_redis_backend():
    """Tests "clear_cache_task" does not attempt to clear not redis backend."""

    mock_backend = MagicMock()
    mock_redis = AsyncMock()
    mock_backend.redis = mock_redis

    with patch.object(FastAPICache, "get_backend", return_value=mock_backend):
        await clear_cache_task()

        mock_backend.redis.flushdb.assert_not_awaited()
