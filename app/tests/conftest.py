from collections.abc import AsyncGenerator

import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Base, db_connector
from core.models.db_connector import DataBaseConnector
from main import app

test_db_connector = DataBaseConnector(
    url=settings.test_pg_db.postgres_url.unicode_string(),
    echo=settings.test_pg_db.echo_sql,
    echo_pool=settings.test_pg_db.echo_pool,
    pool_size=settings.test_pg_db.pool_size,
    max_overflow=settings.test_pg_db.max_overflow,
)


@pytest_asyncio.fixture(scope="function")
async def start_db() -> None:
    """Inits and tears down the database by recreating tables for testing."""

    async with test_db_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await test_db_connector.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a fresh database session for each test function."""

    async with test_db_connector.session_factory() as testing_session:
        yield testing_session


@pytest_asyncio.fixture(scope="function")
async def cache() -> AsyncGenerator[None, None]:
    """Inits in-memory cache and clear it for testing."""

    namespace = "test_cache"
    FastAPICache.init(InMemoryBackend(), prefix=namespace)

    yield

    backend = FastAPICache.get_backend()
    await backend.clear(namespace=namespace)


@pytest_asyncio.fixture(scope="function")
async def client(start_db, cache) -> AsyncGenerator[AsyncClient, None]:
    """Provides async client for testing, overrides session to use testing database,
    inits and clear in-memory cache for tests.

    Args:
        start_db: Fixture to recreate testing database
        cache: Fixture to init and clear testing in-memory cache
    """

    app.dependency_overrides[db_connector.get_session] = test_db_connector.get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/api/v1/trade-results",
    ) as client:
        yield client
