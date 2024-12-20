from datetime import date

import pytest
from fastapi import status
from httpx import AsyncClient

from core.models import SpimexTradeResult
from core.schemas import DynamicsFilterParams, TradeResultOut

from .fixtures import five_test_results

pytestmark = pytest.mark.asyncio(loop_scope="package")
URL = "/dynamics"


@pytest.mark.parametrize("days_from_now", [i for i in range(5)])
async def test_without_optional_params(
    client: AsyncClient, five_test_results: list[SpimexTradeResult], days_from_now: int
) -> None:
    """Tests the '/dynamics' endpoing without optional query params.

    Args:
        client (AsyncClient): Test client to make requests
        five_test_results (list[SpimexTradeResult]): A list of test trade results
        model objects
        days_from_now (int): Days to current day from start_day parameter
    """

    start_date_param = five_test_results[days_from_now].date
    params = DynamicsFilterParams(start_date=start_date_param)

    response = await client.get(URL, params=params.model_dump())
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == days_from_now + 1

    trade_results = [TradeResultOut(**item) for item in response_json]

    for i, trade_result in enumerate(trade_results):
        result_model = five_test_results[i]
        assert trade_result.id == result_model.id
        assert trade_result.exchange_product_id == result_model.exchange_product_id
        assert trade_result.exchange_product_name == result_model.exchange_product_name
        assert trade_result.delivery_basis_id == result_model.delivery_basis_id
        assert trade_result.delivery_basis_name == result_model.delivery_basis_name
        assert trade_result.delivery_type_id == result_model.delivery_type_id
        assert trade_result.volume == result_model.volume
        assert trade_result.total == result_model.total
        assert trade_result.count == result_model.count
        assert trade_result.date == result_model.date
        assert trade_result.created_on == result_model.created_on
        assert trade_result.updated_on == result_model.updated_on


@pytest.mark.parametrize("trade_result_num", [i for i in range(1, 6)])
async def test_with_optional_params(
    client: AsyncClient,
    five_test_results: list[SpimexTradeResult],
    trade_result_num: int,
) -> None:
    """Tests the '/dynamics' endpoint with "DynamicsFilterParams" query parameters.

    Args:
        client (AsyncClient): Test client to make requests
        five_test_results (list[SpimexTradeResult]): A list of test trade results
        model objects
        trade_result_num (int): Integer to take test trade result model
    """

    result_model = five_test_results[-trade_result_num]

    params = DynamicsFilterParams(
        start_date=result_model.date,
        oil_id=result_model.oil_id,
        delivery_type_id=result_model.delivery_type_id,
        delivery_basis_id=result_model.delivery_basis_id,
    )

    response = await client.get(URL, params=params.model_dump())
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1

    trade_result = TradeResultOut(**response_json[0])
    assert trade_result.id == result_model.id
    assert trade_result.exchange_product_id == result_model.exchange_product_id
    assert trade_result.exchange_product_name == result_model.exchange_product_name
    assert trade_result.delivery_basis_id == result_model.delivery_basis_id
    assert trade_result.delivery_basis_name == result_model.delivery_basis_name
    assert trade_result.delivery_type_id == result_model.delivery_type_id
    assert trade_result.volume == result_model.volume
    assert trade_result.total == result_model.total
    assert trade_result.count == result_model.count
    assert trade_result.date == result_model.date
    assert trade_result.created_on == result_model.created_on
    assert trade_result.updated_on == result_model.updated_on


async def test_cache(client: AsyncClient) -> None:
    """Tests cache for the '/dynamics' endpoint.

    Sends tree requests to endpoint and checks cache headers in the responses.
    The second request gets data from cache.

    Args:
        client (AsyncClient): Test client to make requests to the app
    """
    params = {
        "start_date": str(date.today()),
    }

    response_miss = await client.get(URL, params=params)
    assert response_miss.status_code == status.HTTP_200_OK

    response_hit = await client.get(URL, params=params)
    assert response_hit.status_code == status.HTTP_200_OK

    assert response_miss.headers.get("x-fastapi-cache") == "MISS"
    assert response_hit.headers.get("x-fastapi-cache") == "HIT"

    params["start_date"] = str(date(year=2000, month=1, day=1))
    response_param_miss = await client.get(URL, params=params)
    assert response_param_miss.status_code == status.HTTP_200_OK

    assert response_param_miss.headers.get("x-fastapi-cache") == "MISS"
