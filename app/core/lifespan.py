from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from core.models import db_connector
from core.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages the fastapi application's lifespan handling startup and shutdown events.

    on startup:
        1) inits redis for FastAPICache with redis backend
    on shutdown:
        1) closes database connection

    Args:
        app (FastAPI): The FastAPI application instance

    Returns:
        AsyncGenerator[None, None]: AsyncGenerator using by FastAPI
    """

    redis = redis_client.get_client()
    FastAPICache.init(RedisBackend(redis), prefix="main-cache")

    yield

    await db_connector.dispose()
