from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI

from core.lifespan import lifespan


@pytest.mark.asyncio
async def test_lifespan():
    """Tests lifespan function."""

    mock_redis = MagicMock()
    mock_fastapi_cache = MagicMock()
    mock_redis_backend = MagicMock()
    mock_db_connector = AsyncMock()

    with (
        patch("core.lifespan.redis_client.get_client", return_value=mock_redis),
        patch("core.lifespan.RedisBackend", return_value=mock_redis_backend),
        patch("core.lifespan.FastAPICache.init", mock_fastapi_cache.init),
        patch("core.lifespan.db_connector", mock_db_connector),
    ):
        app = FastAPI(lifespan=lifespan)

        async with lifespan(app):
            mock_fastapi_cache.init.assert_called_once_with(
                mock_redis_backend, prefix="main-cache"
            )

        mock_db_connector.dispose.assert_awaited_once()
