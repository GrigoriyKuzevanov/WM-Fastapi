import pytest
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
    assert response.status_code == 200

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
