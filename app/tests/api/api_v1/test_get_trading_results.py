import pytest
from httpx import AsyncClient

from core.models import SpimexTradeResult
from core.schemas import TradeResultOut, TradingFilterParams

from .fixtures import five_test_results

pytestmark = pytest.mark.asyncio(loop_scope="package")
URL = "/"


async def test_without_params(
    client: AsyncClient, five_test_results: list[SpimexTradeResult]
) -> None:
    """Tests the '/' endpoing without query params.

    Args:
        client (AsyncClient): Test client to make requests
        five_test_results (list[SpimexTradeResult]): A list of test trade results
        model objects
    """

    response = await client.get(URL)

    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json) == 5

    for i, resp_result in enumerate(response_json):
        trade_result = TradeResultOut(**resp_result)
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


async def test_with_params(
    client: AsyncClient, five_test_results: list[SpimexTradeResult]
) -> None:
    """Tests the '/' endpoint with "TradingFilterParams" query parameters.

    Args:
        client (AsyncClient): Test client to make requests
        five_test_results (list[SpimexTradeResult]): A list of test trade results
        model objects
    """

    for result_model in five_test_results:
        params = TradingFilterParams(
            oil_id=result_model.oil_id,
            delivery_type_id=result_model.delivery_type_id,
            delivery_basis_id=result_model.delivery_basis_id,
        )

        response = await client.get(URL, params=params.model_dump())
        assert response.status_code == 200

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
    """Tests cache for the '/' endpoint.

    Sends tree requests to endpoint and checks cache headers in the responses.
    The second request gets data from cache.

    Args:
        client (AsyncClient): Test client to make requests to the app
    """

    response_miss = await client.get(URL)
    assert response_miss.status_code == 200

    response_hit = await client.get(URL)
    assert response_hit.status_code == 200

    assert response_miss.headers.get("x-fastapi-cache") == "MISS"
    assert response_hit.headers.get("x-fastapi-cache") == "HIT"

    response_param_miss = await client.get(URL, params={"limit": 1})
    assert response_param_miss.status_code == 200

    assert response_param_miss.headers.get("x-fastapi-cache") == "MISS"
