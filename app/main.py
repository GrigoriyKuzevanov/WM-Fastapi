from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api import api_router
from core.config import settings
from core.models import db_connector
from core.redis import get_redis_cache


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages the fastapi application's lifespan handling startup and shutdown events.

    on startup: inits redis for FastAPICache with redis backend
    on shutdown: closes database connection

    Args:
        app (FastAPI): The FastAPI application instance

    Returns:
        AsyncGenerator[None, None]: AsyncGenerator using by FastAPI
    """

    redis = await get_redis_cache()
    FastAPICache.init(RedisBackend(redis), prefix="main-cache")

    yield

    await db_connector.dispose()


app = FastAPI(
    lifespan=lifespan,
)
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)


if __name__ == "__main__":
    uvicorn.run(
        app=settings.run.app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
