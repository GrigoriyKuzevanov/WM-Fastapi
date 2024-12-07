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
    mock_scheduler = MagicMock()
    mock_db_connector = AsyncMock()

    with (
        patch("core.lifespan.get_redis_cache", return_value=mock_redis),
        patch("core.lifespan.RedisBackend", return_value=mock_redis_backend),
        patch("core.lifespan.FastAPICache.init", mock_fastapi_cache.init),
        patch("core.lifespan.scheduler", mock_scheduler),
        patch("core.lifespan.db_connector", mock_db_connector),
    ):
        app = FastAPI(lifespan=lifespan)

        async with lifespan(app):
            mock_fastapi_cache.init.assert_called_once_with(
                mock_redis_backend, prefix="main-cache"
            )
            mock_scheduler.add_job.assert_called_once()
            mock_scheduler.start.assert_called_once()

        mock_scheduler.shutdown.assert_called_once()
        mock_db_connector.dispose.assert_awaited_once()
