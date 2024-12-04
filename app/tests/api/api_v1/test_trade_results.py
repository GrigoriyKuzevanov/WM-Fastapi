import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_last_trading_dates_cache(client: AsyncClient) -> None:
    """Tests cache for the '/last_dates' endpoint.

    Sends two requests to endpoint and checks cache headers in the responses. The second
    request gets data from cache.

    Args:
        client (AsyncClient): Test client to make requests to the app
    """

    response_miss = await client.get("/last-dates")
    assert response_miss.status_code == 200

    response_hit = await client.get("/last-dates")
    assert response_hit.status_code == 200

    assert response_miss.headers.get("x-fastapi-cache") == "MISS"
    assert response_hit.headers.get("x-fastapi-cache") == "HIT"
