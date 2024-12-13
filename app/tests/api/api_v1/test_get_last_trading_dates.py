import pytest
from fastapi import status
from httpx import AsyncClient

from core.models import SpimexTradeResult

from .fixtures import five_test_results

pytestmark = pytest.mark.asyncio(loop_scope="package")
URL = "/last-dates"


async def test_without_params(
    client: AsyncClient, five_test_results: list[SpimexTradeResult]
) -> None:
    """Tests the '/last-dates' endpoint without query params.

    Args:
        client (AsyncClient): Test client to make requests
        five_test_dates_results (list[SpimexTradeResult]): A list of test trade results
        model objects
    """

    response = await client.get(URL)

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1

    assert response_json[0] == str(five_test_results[0].date)


@pytest.mark.parametrize("days", [i for i in range(1, 6)])
async def test_with_days_params(
    days: int, client: AsyncClient, five_test_results: list[SpimexTradeResult]
) -> None:
    """Tests the '/last-dates' endpoint with "days" query parameter.

    Args:
        days (int): "days" query parameter value
        client (AsyncClient): Test client to make requests
        five_test_dates_results (list[SpimexTradeResult]):  A list of test trade results
        model objects
    """

    response = await client.get(URL, params={"days": days})

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()

    assert len(response_json) == days
    for i, resp_date in enumerate(response_json):
        assert resp_date == str(five_test_results[i].date)


async def test_cache(client: AsyncClient) -> None:
    """Tests cache for the '/last_dates' endpoint.

    Sends tree requests to endpoint and checks cache headers in the responses.
    The second request gets data from cache.

    Args:
        client (AsyncClient): Test client to make requests to the app
    """

    response_miss = await client.get(URL)
    assert response_miss.status_code == status.HTTP_200_OK

    response_hit = await client.get(URL)
    assert response_hit.status_code == status.HTTP_200_OK

    assert response_miss.headers.get("x-fastapi-cache") == "MISS"
    assert response_hit.headers.get("x-fastapi-cache") == "HIT"

    response_param_miss = await client.get(URL, params={"days": 1})
    assert response_param_miss.status_code == status.HTTP_200_OK

    assert response_param_miss.headers.get("x-fastapi-cache") == "MISS"
