from contextlib import asynccontextmanager
from typing import AsyncGenerator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from core.config import settings
from core.models import db_connector
from core.redis import clear_cache_task, redis_client

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages the fastapi application's lifespan handling startup and shutdown events.

    on startup:
        1) inits redis for FastAPICache with redis backend
        2) adds job for clearing cache and starts apscheduler
    on shutdown:
        1) shuts down apscheduler
        2) closes database connection

    Args:
        app (FastAPI): The FastAPI application instance

    Returns:
        AsyncGenerator[None, None]: AsyncGenerator using by FastAPI
    """

    redis = redis_client.get_client()
    FastAPICache.init(RedisBackend(redis), prefix="main-cache")

    scheduler.add_job(
        clear_cache_task,
        CronTrigger(
            hour=settings.clear_cache.hour,
            minute=settings.clear_cache.minute,
            timezone=settings.clear_cache.timezone,
        ),
        id="crear_cache_job",
        replace_existing=True,
    )
    scheduler.start()

    yield

    scheduler.shutdown()

    await db_connector.dispose()
