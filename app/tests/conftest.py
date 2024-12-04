from collections.abc import AsyncGenerator

import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Base
from core.models.db_connector import DataBaseConnector
from main import app

test_db_connector = DataBaseConnector(
    url=settings.test_pg_db.postgres_url.unicode_string(),
    echo=settings.test_pg_db.echo_sql,
    echo_pool=settings.test_pg_db.echo_pool,
    pool_size=settings.test_pg_db.pool_size,
    max_overflow=settings.test_pg_db.max_overflow,
)


@pytest_asyncio.fixture(scope="session")
async def start_db() -> None:
    """Inits and tears down the database by recreating tables for testing. Runs once per
    testing session.
    """

    async with test_db_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await test_db_connector.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a fresh database session for each test function. Runs once per test."""

    yield test_db_connector.get_session()


@pytest_asyncio.fixture(scope="session")
async def cache() -> None:
    """Inits the in-memory cache for the test session. Runs once per session."""

    FastAPICache.init(InMemoryBackend())


@pytest_asyncio.fixture(scope="session")
async def client(start_db, cache) -> AsyncGenerator[AsyncClient, None]:
    """Provides async client for testing, overrides session to use testing database,
    inits in-memory cache for tests. Runs once per session.

    Args:
        start_db: Fixture to recreate testing database
        cache: Fixture to init in-memory cache
    """

    async def override_session():
        yield test_db_connector.get_session()

    app.dependency_overrides[session] = override_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/api/v1/trade-results",
    ) as client:
        yield client
